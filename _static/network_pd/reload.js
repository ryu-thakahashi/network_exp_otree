console.log("reload.js loaded");
// 5秒ごとにページをリロード
setInterval(function () {
	console.log("5秒経ったからリロード！🔄");
	window.location.reload();
}, 5000);
