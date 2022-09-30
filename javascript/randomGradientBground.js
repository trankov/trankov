/*
   Functions for generating a random gradient background. Optimized for white text.
   Usage: MyElement.style.background = randGradBG();
 */

// Function of getting random array element (such as random.choice() in Python)
const randArr = (arr) => {
    return arr[~~(Math.random() * arr.length)];
};

// Random RGB/HEX, max = threshold value (to prevent light shades)
const randHex = (max = 16) => {
    return '#000000'.replace(/0/g, function () {
        return (~~(Math.random() * max)).toString(16);
    });
};

// Random direction in terms of CSS3 <position>
const randPosition = () => {
    return randArr(['top', 'bottom', '']) + ' ' + randArr(['left', 'right']);
};

// Random angle 0-360deg
const randAngle = () => {
    return ~~(Math.random() * 360) + 'deg';
};

// Random chain of HEX colors
const randHexChain = (max = 16) => {
    // Is this 2 or 3 colors in the chain?
    iter = ~~(Math.random() * 2) + 2;
    let chain = '';

    // Last element added in return to prevent trailing comma
    for (let i = 1; i <= iter - 1; i++) {
        chain += randHex(max) + ', ';
    }
    return chain + randHex(max);
};

// Build linear gradient
const randLinearGradient = () => {
    return 'linear-gradient(' + randAngle() + ', ' + randHexChain(14) + ')';
};

// Build radial gradient
const randRadialGradient = () => {
    /*
    possible = [
        "ellipse at " + randPosition() + ", " + randHex(14) + ", transparent",
        randHexChain(14) + randArr([", transparent"])
    ];

    In practice, the above turned out to be too redundant/abundand.
    In production version, it's better to return a bit simpler result.
    */

    return (
        'radial-gradient(ellipse at ' +
        randPosition() +
        ', ' +
        randHex(14) +
        ', transparent)'
    );
};

// Build background
const randGradBG = () => {
    // Is this 2 or 3 colors in the chain?
    iter = ~~(Math.random() * 2) + 2;
    let chain = '';

    // For prevent a trailing comma, last element added at return
    for (let i = 1; i <= iter - 1; i++) {
        let rlg = randLinearGradient();
        let rrg = randRadialGradient();
        chain += randArr([rlg, rrg]) + ', ';
    }
    let rlg = randLinearGradient();
    let rrg = randRadialGradient();
    return chain + randArr([rlg, rrg]);
};
