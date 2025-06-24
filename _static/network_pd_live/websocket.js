import {
	set_my_color,
	set_my_payoff,
	set_neighbor_color,
	set_neighbor_payoffs,
	simulation,
	link,
	node,
	label,
} from "./plot_network.js";

// set_my_color(1);

function liveRecv(data) {
	console.log("received a message!", data);
	const state = data.type;
	change_display_state(data, state);
}

function change_display_state(data, state) {
	// 画面の状態を変更する処理
	console.log("Changing display state to:", state);
	if (state === "all_players_decided") {
		display_all_players_decided(data);
	} else if (state === "all_players_confirmed") {
		// display_all_players_confirmed();
	} else if (state === "game_finished") {
		// display_game_finished();
	} else {
		console.warn("Unknown display state:", state);
	}
}

function display_all_players_decided() {
	// すべてのプレイヤーが決定した場合の処理
	console.log("Displaying all players' decisions.");
}
