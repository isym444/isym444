/* console.log("JavaScript is connected!");
let listItems = document.querySelectorAll("li");
console.log(listItems);
console.log("Number of nested list items: " + listItems.length); */
/* var test = document.getElementsByClassName('ul')[0];
var nested = test.getElementsByTagName("OL").length + test.getElementsByTagName("UL").length;
console.log(nested);
console.log(test); */

let temp = 1;

function findMaxDepth(element, depth) {
	let maxDepth = depth;
	temp = Math.max(maxDepth, temp);
	/* console.log(element.children.length);
	console.log("marker"); */
	if (element.children.length != 0) {
		/* console.log(element.children[0].localName); */
	}
	if (element.children.length != 0) {
		for (let i = 0; i < element.children.length; i++) {
			let child = element.children[i];
			//findMaxDepth(child, depth + 1);
			if (child.localName === "li" || child.localName === "div") {
				findMaxDepth(child, depth);
			}
			if (child.localName === "ul" || child.localName === "ol") {
				findMaxDepth(child, depth + 1);
				//maxDepth = Math.max(maxDepth, childDepth);
			}
		}
	}
	return maxDepth;
}

let list = document.querySelector("ul, ol");
findMaxDepth(list, 1)
console.log(list);
if (list) {
	console.log("Maximum depth of nested list items: " + temp);
} else {
	console.error("No 'ul' or 'ol' element found in the document");
}

