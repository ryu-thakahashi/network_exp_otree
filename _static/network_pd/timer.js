// 定数
const FULL_DASH_ARRAY = 2 * Math.PI * 45; // ≒283
const TIME_LIMIT = 20; // 秒
const WARNING_THRESHOLD = 10;
const ALERT_THRESHOLD = 5;

const COLOR_CODES = {
	info: "info",
	warning: "warning",
	alert: "alert",
};

// 状態
let timePassed = 0;
let timeLeft = TIME_LIMIT;
let timerInterval = null;

// 初期描画
document.getElementById("base-timer-label").innerHTML = formatTime(timeLeft);

// タイマー開始
startTimer();

const START_TIME = js_vars.start_time * 1000;
function calcTimeLeft() {
	const startTime = new Date(START_TIME);
	console.log("startTime", startTime);

	const now = new Date();
	console.log("now", now);

	const elapsedTime = Math.floor((now - startTime) / 1000);
	console.log("elapsedTime", elapsedTime);

	const timeLeft = TIME_LIMIT - elapsedTime;
	console.log("timeLeft", timeLeft);

	return timeLeft;
}

function startTimer() {
	timerInterval = setInterval(() => {
		// timePassed += 1;
		// timeLeft = TIME_LIMIT - timePassed;
		timeLeft = calcTimeLeft();

		// ラベル更新
		document.getElementById("base-timer-label").innerHTML =
			formatTime(timeLeft);

		// 円弧長更新
		setCircleDasharray();

		// 色変更
		setRemainingPathColor(timeLeft);

		if (timeLeft <= 0) {
			clearInterval(timerInterval);
		}
	}, 1000);
}

function formatTime(sec) {
	const m = Math.floor(sec / 60);
	const s = sec % 60;
	return `${m}:${s < 10 ? "0" : ""}${s}`;
}

function push_A_btn() {
	document.getElementById("btn-A").click();
}

function push_B_btn() {
	document.getElementById("btn-B").click();
}
function setRemainingPathColor(timeLeft) {
	if (timeLeft <= 0) {
		if (Math.random() < 0.5) {
			// push_A_btn();
		} else {
			// push_B_btn();
		}
	}

	const path = document.getElementById("base-timer-path-remaining");
	path.classList.remove(
		COLOR_CODES.info,
		COLOR_CODES.warning,
		COLOR_CODES.alert
	);

	if (timeLeft <= ALERT_THRESHOLD) {
		path.classList.add(COLOR_CODES.alert);
	} else if (timeLeft <= WARNING_THRESHOLD) {
		path.classList.add(COLOR_CODES.warning);
	} else {
		path.classList.add(COLOR_CODES.info);
	}
}

function calculateTimeFraction() {
	const rawFraction = timeLeft / TIME_LIMIT;
	// 少し補正して見た目スムーズに
	return rawFraction - (1 / TIME_LIMIT) * (1 - rawFraction);
}

function setCircleDasharray() {
	const circleDasharray = `${(
		calculateTimeFraction() * FULL_DASH_ARRAY
	).toFixed(0)} ${FULL_DASH_ARRAY}`;
	document
		.getElementById("base-timer-path-remaining")
		.setAttribute("stroke-dasharray", circleDasharray);
}
