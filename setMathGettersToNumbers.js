for (let n of ['ceil', 'floor', 'round']) {
    Number.prototype.__defineGetter__(
        n, 
        function(){
            return Math[n](this)
        }
    );
}

console.log(22.11.ceil, 22.11.round,  22.11.floor);
