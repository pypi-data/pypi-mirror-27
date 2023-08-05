

function getCellsFromMetadata(nbCells) {

	let arrCell = [];
	for (let [i, nbCell] of nbCells.entries()) {
		if (nbCell.metadata.autorun) {
			arrCell.push(i);
		}
	}

	return arrCell;
}
