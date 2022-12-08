fetch("https://adventofcode.com/2022/day/1/input").then(data => data.text()).then(text => { 
    console.log(text.trim().split("\n\n").map(group => { 
        return group.split("\n").reduce((acc, val) => { 
            return acc + parseInt(val)
        }, 0)
    }).sort().reverse().reduce(
        (acc, val, index) => { console.log(val); return index < 3 ? acc + val : acc}, 0))
})