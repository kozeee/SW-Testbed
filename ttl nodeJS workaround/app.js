//async sleep function definitely (not) from stackoverflow
//we are creating a promise to execute the rest of our function when our setTimeout resolves in (x) ms
//promises essentially create a "snapshot" of a function, meaning we can pass variables, and then safely alter them without breaking our existing promises
//important to note that promises are non-blocking but can only be used in async functions!

async function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

//because a practical demo would require creating a bunch of fax requests, instead we will just print to the console
//consoler takes a text and timer argument, and logs the timer to the console. All 3 "Fax will send in `timer` MS" will print to the console first.
//now we will await our `sleep` function for `timer` milliseconds. this creates our promise to print to the console.
async function consoler(text,timer,iter){
console.log ("Fax will send in ",timer," milliseconds");
console.time(iter);
await sleep(timer);
console.log(text);
console.timeEnd(iter);
}

console.time("time take to create all 3 promises")
// setting up our variables
let timer = "0";
let text = "empty";
let iter = "0";

//here we set our variables to their first values
iter = "1";
timer = "7000";
text = "I was first, but my promise took: "+timer+" ms";
//when we call our `consoler` function, the `text` and `timer` we pass will be preserved in our promise similar to how we could preserve `to`,`from`, and `mediaurl` when retrying a fax.
consoler(text,timer,iter);

// this will be our second promise, it will execute second.
iter = "2";
timer = "6000";
text = "I am in the Middle. My timer expired in "+timer+" ms";
consoler(text,timer,iter);

// this will be the last promise we create, but the first to execute because it's timer resolves first.
iter = "3";
timer="2000";
text = "I was last, but my promise expired in "+timer+" ms";
consoler(text,timer,iter);
console.timeEnd("time take to create all 3 promises")
