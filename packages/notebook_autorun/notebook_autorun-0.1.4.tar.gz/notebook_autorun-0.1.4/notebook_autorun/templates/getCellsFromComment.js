

function getCellsFromComment(nbCells, commentFlag) {

	let arrCell = [];
	for (let [i, nbCell] of nbCells.entries()) {

		let text = nbCell.get_text();
		let arrText = text.split('\n');
		let isFlag = false;
		for (let line of arrText) {
			line = line.trim();
			if (line.startsWith('#')) {
				let found = line.indexOf(commentFlag) > -1;
				if (found) {
					isFlag = true;
				}
			}
		}
		if (isFlag) {
			arrCell.push(i);
		}
	}
	return arrCell;
}
