const svg_obj = document.getElementById("network-svg");
const svg_w = svg_obj.getAttribute("width");
const svg_h = svg_obj.getAttribute("height");
// const { svg_w, svg_h } = svg_obj.node().getBoundingClientRect();

const svg_w_half = svg_w + 400;
const l1_w = 280;
const l2_w = 230;
const l3_w = 150;
const svg_h_half = svg_h / 2;
const l1_h = 50;
const l2_h = 140;
const l3_h = 220;

const nei_nodes = [
	{ id: "left_3", fx: svg_w_half - l3_w, fy: l3_h },
	{ id: "right_3", fx: svg_w_half + l3_w, fy: l3_h },
	{ id: "left_2", fx: svg_w_half - l2_w, fy: l2_h },
	{ id: "right_2", fx: svg_w_half + l2_w, fy: l2_h },
	{ id: "left_1", fx: svg_w_half - l1_w, fy: l1_h },
	{ id: "right_1", fx: svg_w_half + l1_w, fy: l1_h },
];

const color_dict = {
	gray: "#808080",
	select_A: "#198754",
	select_B: "#ffc107",
};
const nodes = [
	{ id: "center", fx: svg_w_half, fy: 250, color: color_dict.gray },
];

const show_payoff = js_vars.show_payoffs;

function set_my_color(self_action) {
	if (self_action === undefined) {
		nodes[0].color = color_dict.gray;
		return;
	}

	if (self_action === 1) {
		nodes[0].color = color_dict.select_A;
	} else if (self_action === 0) {
		nodes[0].color = color_dict.select_B;
	}
}
const self_action = js_vars.self_action;
set_my_color(self_action);

function set_my_payoff(show_payoff, self_payoff) {
	console.log("show_payoff", show_payoff);
	console.log("self_payoff", self_payoff);

	// ガード節
	if (show_payoff === undefined || show_payoff === "false") {
		return;
	} else if (self_payoff === undefined) {
		return;
	}

	nodes[0].payoff = self_payoff;
}
const self_payoff = js_vars.self_payoff;
set_my_payoff(show_payoff, self_payoff);

function set_neighbor_color(nei_actions) {
	for (let i = 0; i < js_vars.num_of_k; i++) {
		const node_info = nei_nodes[i];
		if (nei_actions) {
			node_info.color =
				js_vars.actions[i] === 1 ? color_dict.select_A : color_dict.select_B;
		} else {
			node_info.color = color_dict.gray;
		}
		nodes.push(node_info);
	}
}
const nei_actions = js_vars.actions;
set_neighbor_color(nei_actions);

function set_neighbor_payoffs(show_payoff, nei_payoffs) {
	function set_payoffs(show_payoff, payoffs) {
		if (show_payoff === false) {
			payoffs = ["?", "?", "?", "?"];
		}

		for (let i = 0; i < js_vars.num_of_k; i++) {
			const node_info = nei_nodes[i];
			if (payoffs) {
				node_info.payoff = payoffs[i];
			} else {
				node_info.payoff = 0;
			}
			nodes.push(node_info);
		}
	}
	console.log("show_payoff", show_payoff);
	console.log("nei_payoffs", nei_payoffs);

	// ガード節
	if (show_payoff === undefined) {
		return;
	}
	if (nei_payoffs === undefined) {
		return;
	}

	set_payoffs(show_payoff, nei_payoffs);
}
const nei_payoffs = js_vars.payoffs;
set_neighbor_payoffs(show_payoff, nei_payoffs);

const links = [];
for (let i = 1; i < nodes.length; i++) {
	links.push({
		source: "center",
		target: nodes[i].id,
	});
}

const svg = d3.select("svg");
const width = +svg.attr("width");
const height = +svg.attr("height");

const simulation = d3
	.forceSimulation(nodes)
	.force(
		"link",
		d3
			.forceLink(links)
			.id((d) => d.id)
			.distance(120)
	)
	.force("charge", d3.forceManyBody().strength(-300));

const link = svg
	.append("g")
	.attr("stroke", "#444")
	.attr("stroke-width", 5)
	.selectAll("line")
	.data(links)
	.join("line");

const node = svg
	.append("g")
	.selectAll("circle")
	.data(nodes)
	.join("circle")
	.attr("fill", (d) => d.color)
	.attr("r", 30);

const label = svg
	.append("g")
	.attr("font-family", "sans-serif")
	.attr("font-size", 35)
	.attr("text-anchor", "middle")
	.attr("pointer-events", "none")
	.selectAll("text")
	.data(nodes)
	.join("text")
	.text((d) => d.payoff)
	.attr("fill", "#fff"); // ←ココ！白文字🌟

simulation.on("tick", () => {
	link
		.attr("x1", (d) => d.source.x)
		.attr("y1", (d) => d.source.y)
		.attr("x2", (d) => d.target.x)
		.attr("y2", (d) => d.target.y);

	node.attr("cx", (d) => d.x).attr("cy", (d) => d.y);

	label.attr("x", (d) => d.x).attr("y", (d) => d.y + 10);
});
