/* CONSTANTS AND FUNCTION POINTERS */
min = Math.min
max = Math.max
round = Math.round
floor = Math.floor
random = Math.random
cos = Math.cos
sin = Math.sin
abs = Math.abs
pow = Math.pow
sqrt = Math.sqrt
PI = Math.PI

/* UTIL FUNCTIONS */
function roundToTenThousandth(n) {
    return round(n * 10000) / 10000;
}

function roundToHundredth(n) {
    return round(n * 100) / 100;
}

function roundToTenth(n) {
    return round(n * 10) / 10;
}