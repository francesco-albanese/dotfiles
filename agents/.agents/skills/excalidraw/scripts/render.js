#!/usr/bin/env node
// excalidraw-render: emit .excalidraw files from skeleton-JSON inputs.
// Usage:
//   node render.js --skeleton <input.json> --out <output.excalidraw>

import { readFileSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";
import { randomBytes } from "node:crypto";

const STYLE = {
	roughness: 1,
	fontFamily: 1,
	strokeWidth: 2,
	strokeColor: "#1e1e1e",
	bgDefault: "transparent",
	fillStyle: "solid",
	fontSize: 20,
};

const ROLE_BG = {
	"entry-point": "#a5d8ff",
	core: "#b2f2bb",
	business: "#b2f2bb",
	data: "#ffc9c9",
	persistence: "#ffc9c9",
	infra: "#fab005",
	config: "#fab005",
	external: "#ced4da",
	integration: "#ced4da",
	"cross-cutting": "#7950f288",
	group: "transparent",
};

const argv = parseArgs(process.argv.slice(2));
if (!argv.out) die("missing --out <file.excalidraw>");
if (!argv.skeleton) die("need --skeleton <file.json>");

const elements = fromSkeleton(
	JSON.parse(readFileSync(resolve(argv.skeleton), "utf8")),
);

const file = {
	type: "excalidraw",
	version: 2,
	source: "https://excalidraw.com",
	elements,
	appState: { gridSize: null, viewBackgroundColor: "#ffffff" },
	files: {},
};

writeFileSync(resolve(argv.out), JSON.stringify(file, null, 2));
console.log(`wrote ${argv.out} (${elements.length} elements)`);

// ---------- skeleton path ----------
// Accepts ExcalidrawElementSkeleton-shaped objects:
//   {type:"rectangle", id?, x, y, width, height, label?:{text,fontSize?}, role?, backgroundColor?}
//   {type:"ellipse"|"diamond", ...}
//   {type:"text", x, y, text, fontSize?, width?, height?}
//   {type:"arrow", x?, y?, start:{id}|{x,y}, end:{id}|{x,y}, label?:{text}, points?}
//   {type:"line",  x?, y?, start:{...}, end:{...}, points?}

function fromSkeleton(skeleton) {
	const out = [];
	const byId = new Map();

	// Pass 1: shapes + their bound text labels.
	for (const el of skeleton) {
		if (
			el.type === "rectangle" ||
			el.type === "ellipse" ||
			el.type === "diamond"
		) {
			const id = el.id || newId();
			const shape = baseElement({
				...el,
				id,
				type: el.type,
				backgroundColor:
					el.backgroundColor || ROLE_BG[el.role] || STYLE.bgDefault,
				fillStyle:
					el.fillStyle || (el.backgroundColor || el.role ? "solid" : "hachure"),
			});
			shape.boundElements = [];
			out.push(shape);
			byId.set(id, shape);

			if (el.label?.text) {
				const labelId = newId();
				const label = baseElement({
					id: labelId,
					type: "text",
					x: shape.x + shape.width / 2,
					y: shape.y + shape.height / 2,
					width: 0,
					height: 0,
					backgroundColor: "transparent",
					fillStyle: "solid",
					strokeWidth: 1,
				});
				label.text = el.label.text;
				label.originalText = el.label.text;
				label.fontSize = el.label.fontSize || STYLE.fontSize;
				label.fontFamily = el.label.fontFamily || STYLE.fontFamily;
				label.textAlign = "center";
				label.verticalAlign = "middle";
				label.containerId = id;
				label.lineHeight = 1.25;
				const measured = measureText(label.text, label.fontSize);
				label.width = measured.width;
				label.height = measured.height;
				label.x = shape.x + (shape.width - measured.width) / 2;
				label.y = shape.y + (shape.height - measured.height) / 2;
				label.baseline = Math.round(label.fontSize * 0.85);
				shape.boundElements.push({ id: labelId, type: "text" });
				out.push(label);
				byId.set(labelId, label);
			}
		} else if (el.type === "text") {
			const id = el.id || newId();
			const fontSize = el.fontSize || STYLE.fontSize;
			const measured =
				el.width && el.height
					? { width: el.width, height: el.height }
					: measureText(el.text, fontSize);
			const text = baseElement({
				...el,
				id,
				type: "text",
				width: measured.width,
				height: measured.height,
				backgroundColor: "transparent",
				fillStyle: "solid",
				strokeWidth: 1,
			});
			text.text = el.text;
			text.originalText = el.text;
			text.fontSize = fontSize;
			text.fontFamily = el.fontFamily || STYLE.fontFamily;
			text.textAlign = el.textAlign || "left";
			text.verticalAlign = el.verticalAlign || "top";
			text.lineHeight = 1.25;
			text.baseline = Math.round(fontSize * 0.85);
			out.push(text);
			byId.set(id, text);
		}
	}

	// Pass 2: arrows + lines (need shape ids resolved).
	for (const el of skeleton) {
		if (el.type !== "arrow" && el.type !== "line") continue;

		const id = el.id || newId();
		const startBinding = bindingFor(el.start, byId);
		const endBinding = bindingFor(el.end, byId);
		const points = computePoints(el, startBinding, endBinding, byId);
		const start = points[0];
		const end = points[points.length - 1];

		const arrow = baseElement({
			...el,
			id,
			type: el.type,
			x: 0, // arrow x/y is anchor; points are relative
			y: 0,
			width: Math.abs(end[0] - start[0]),
			height: Math.abs(end[1] - start[1]),
			backgroundColor: "transparent",
			fillStyle: "solid",
		});
		arrow.x = start[0] === 0 ? 0 : (el.x ?? start[0]);
		arrow.y = start[1] === 0 ? 0 : (el.y ?? start[1]);
		// Re-anchor points relative to arrow.x/y
		arrow.points = points.map(([px, py]) => [px - arrow.x, py - arrow.y]);
		arrow.lastCommittedPoint = null;
		arrow.startBinding = startBinding;
		arrow.endBinding = endBinding;
		arrow.startArrowhead = null;
		arrow.endArrowhead = el.type === "arrow" ? "arrow" : null;
		arrow.elbowed = false;
		out.push(arrow);

		// Wire boundElements on the connected shapes
		if (startBinding)
			addBound(byId.get(startBinding.elementId), { id, type: el.type });
		if (endBinding)
			addBound(byId.get(endBinding.elementId), { id, type: el.type });

		if (el.label?.text) {
			const labelId = newId();
			const fontSize = el.label.fontSize || 16;
			const mid = midpoint(points);
			const measured = measureText(el.label.text, fontSize);
			const label = baseElement({
				id: labelId,
				type: "text",
				x: mid[0] - measured.width / 2,
				y: mid[1] - measured.height / 2,
				width: measured.width,
				height: measured.height,
				backgroundColor: "transparent",
				fillStyle: "solid",
				strokeWidth: 1,
			});
			label.text = el.label.text;
			label.originalText = el.label.text;
			label.fontSize = fontSize;
			label.fontFamily = STYLE.fontFamily;
			label.textAlign = "center";
			label.verticalAlign = "middle";
			label.containerId = id;
			label.lineHeight = 1.25;
			label.baseline = Math.round(fontSize * 0.85);
			arrow.boundElements = [{ id: labelId, type: "text" }];
			out.push(label);
		}
	}

	return out;
}

function bindingFor(end, byId) {
	if (!end || !end.id) return null;
	const target = byId.get(end.id);
	if (!target) return null;
	return { elementId: end.id, focus: 0, gap: 4 };
}

function computePoints(el, startBinding, endBinding, byId) {
	if (Array.isArray(el.points) && el.points.length >= 2) return el.points;

	let sx, sy, ex, ey;
	if (startBinding) {
		const s = byId.get(startBinding.elementId);
		sx = s.x + s.width / 2;
		sy = s.y + s.height / 2;
	} else if (el.start && Number.isFinite(el.start.x)) {
		sx = el.start.x;
		sy = el.start.y;
	} else {
		sx = el.x ?? 0;
		sy = el.y ?? 0;
	}
	if (endBinding) {
		const e = byId.get(endBinding.elementId);
		ex = e.x + e.width / 2;
		ey = e.y + e.height / 2;
	} else if (el.end && Number.isFinite(el.end.x)) {
		ex = el.end.x;
		ey = el.end.y;
	} else {
		ex = (el.x ?? 0) + 100;
		ey = el.y ?? 0;
	}
	return [
		[sx, sy],
		[ex, ey],
	];
}

function midpoint(points) {
	if (points.length === 2) {
		return [
			(points[0][0] + points[1][0]) / 2,
			(points[0][1] + points[1][1]) / 2,
		];
	}
	return points[Math.floor(points.length / 2)];
}

function addBound(el, ref) {
	if (!el) return;
	el.boundElements = el.boundElements || [];
	if (!el.boundElements.find((b) => b.id === ref.id))
		el.boundElements.push(ref);
}

// ---------- element envelope ----------

function baseElement(el) {
	return {
		id: el.id || newId(),
		type: el.type,
		x: el.x ?? 0,
		y: el.y ?? 0,
		width: el.width ?? 0,
		height: el.height ?? 0,
		angle: 0,
		strokeColor: el.strokeColor || STYLE.strokeColor,
		backgroundColor: el.backgroundColor ?? STYLE.bgDefault,
		fillStyle: el.fillStyle || STYLE.fillStyle,
		strokeWidth: el.strokeWidth ?? STYLE.strokeWidth,
		strokeStyle: el.strokeStyle || "solid",
		roughness: el.roughness ?? STYLE.roughness,
		opacity: el.opacity ?? 100,
		groupIds: el.groupIds || [],
		frameId: null,
		roundness:
			el.type === "rectangle"
				? { type: 3 }
				: el.type === "arrow" || el.type === "line"
					? { type: 2 }
					: null,
		seed: rint(),
		version: 1,
		versionNonce: rint(),
		isDeleted: false,
		boundElements: el.boundElements || [],
		updated: Date.now(),
		link: null,
		locked: false,
	};
}

function measureText(text, fontSize) {
	const lines = String(text).split("\n");
	const longest = lines.reduce((m, l) => Math.max(m, l.length), 0);
	// Rough heuristic: ~0.55em per char width for Virgil at fontSize.
	const width = Math.max(40, Math.ceil(longest * fontSize * 0.55));
	const height = Math.ceil(lines.length * fontSize * 1.25);
	return { width, height };
}

function newId() {
	return randomBytes(12).toString("base64url");
}

function rint() {
	return Math.floor(Math.random() * 2_000_000_000);
}

function parseArgs(args) {
	const out = {};
	for (let i = 0; i < args.length; i++) {
		const a = args[i];
		if (a.startsWith("--")) {
			const key = a.slice(2);
			const val =
				args[i + 1] && !args[i + 1].startsWith("--") ? args[++i] : true;
			out[key] = val;
		}
	}
	return out;
}

function die(msg) {
	console.error(`render.js: ${msg}`);
	process.exit(1);
}
