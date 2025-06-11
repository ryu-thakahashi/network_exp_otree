const btnA = document.getElementById("btn-A");
const btnB = document.getElementById("btn-B");

window.onload = function () {
	const form_field = document.getElementById("id_action");
	form_field.value = "";
};

btnA.addEventListener("click", function () {
	disableButtons();
	liveSend({ action: 1 });
});

btnB.addEventListener("click", function () {
	disableButtons();
	liveSend({ action: 0 });
});

function disableButtons() {
	btnA.disabled = true;
	btnB.disabled = true;
}

function liveRecv(data) {
	console.log("received a message!", data);
	const dataType = data.type;
	if (dataType === "all_players_decided") {
		// すべてのプレイヤーが決定した場合，フィードバック画面へ
		console.log("All players have made their decisions.");
	} else if (dataType === "all_players_confirmed") {
		// すべてのプレイヤーが結果を確認した場合，意志決定画面へ
		console.log("All players have confirmed their decisions.");
	} else if (dataType === "game_finished") {
		// ゲームが終了した場合，最終結果を表示
		console.log("Game finished, submitting form.");
		// document.getElementById("form").submit();
	} else {
		console.warn("Unknown message data:", data);
	}
}

window.addEventListener("unload", function () {
	liveSend({ action: 99 });
});

// 例: あなたの liveSend のソケット参照が `socket` だとすると…
window.addEventListener("beforeunload", function (e) {
	// 1) Close フレームを送る
	socket.close(1000, "Normal closure");
	// 2) （オプション）短く待ってからページ離脱
	//    e.preventDefault(); e.returnValue = "";
});
