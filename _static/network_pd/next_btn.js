const nextBtn = document.getElementsByClassName("otree-btn-next")[0];
console.log("nextBtn", nextBtn);

nextBtn.addEventListener("click", function () {
	liveSend({ confirm: 1 });
});

window.addEventListener("unload", function () {
	liveSend({ confirm: 99 });
});
