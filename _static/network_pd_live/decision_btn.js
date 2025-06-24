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
