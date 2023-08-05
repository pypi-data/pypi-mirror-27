

let getCellsFromComment = function (nbCells, commentFlag) {

	let arrCell = [];
	for (let [i, nbCell] of nbCells.entries()) {

		let text = nbCell.get_text();
		
		if (isFlagInComment(text, commentFlag)) {
			arrCell.push(i);
		}
	}
	return arrCell;
};

let isFlagInComment = function (text, flag) {
	let arrText = text.split('\n');
	let isFlag = false;
	for (let line of arrText) {
		line = line.trim();
		if (line.startsWith('#')) {
			let found = line.indexOf(flag) > -1;
			if (found) {
				isFlag = true;
			}
		}
	}
	return isFlag;
};