document.addEventListener("DOMContentLoaded", function () {
	// Aボタン（Cを選択）
	document.getElementById("btn-A").addEventListener("click", function () {
		selectOptionAndSubmit(1);
	});

	// Bボタン（Dを選択）
	document.getElementById("btn-B").addEventListener("click", function () {
		selectOptionAndSubmit(0);
	});
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

	// Next ボタンをクリック
	document.getElementById("next-button").click();
}
