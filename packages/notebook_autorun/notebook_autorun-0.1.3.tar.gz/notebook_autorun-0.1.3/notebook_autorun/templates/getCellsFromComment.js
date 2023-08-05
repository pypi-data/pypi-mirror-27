

function getCellsFromComment(nbCells, commentFlag) {

	let re = `/${commentFlag}/i`;
	let arrCell = [];
	for (let [i, nbCell] of nbCells.entries()) {
		let text = nbCell.get_text();
		let found = text.match(re);
		if (found) {
			arrCell.push(i);
		}
	}

	return arrCell;
}
