const btnA = document.getElementById("btn-A");
const btnB = document.getElementById("btn-B");

btnA.addEventListener("click", function () {
	selectOptionAndSubmit(1);
	liveSend({ action: 1 });
});

btnB.addEventListener("click", function () {
	selectOptionAndSubmit(1);
	liveSend({ action: 0 });
});

function selectOptionAndSubmit(value) {
	// 対応するラジオボタンを選択
	const id = `id_action-${value}`;
	console.log(id);
	let radioButton = document.getElementById(`id_action-${value}`);
	console.log(radioButton);
	if (radioButton) {
		radioButton.checked = true;
	}
}

function liveRecv(data) {
	console.log("received a message!", data);
	let type = data.type;
	if (type === "game_finished") {
		document.getElementById("form").submit();
	}
	// handle other types of messages here..
	// your code goes here
}

window.addEventListener("unload", function () {
	liveSend({ action: 99 });
});
