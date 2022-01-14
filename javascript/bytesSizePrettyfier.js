// Форматирование байт в человеческий вид

function prettySize(bytes, separator = '', postFix = '') {
    if (bytes) {
        const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
        const i = Math.min(parseInt(Math.floor(Math.log(bytes) / Math.log(1024)).toString(), 10), sizes.length - 1);
        const size = (bytes / (1024 ** i)).toFixed(i ? 1 : 0);
        return (`${size}${separator}${sizes[i]}${postFix}`).replace(".",",");
    }
    return 'n/a';
}
