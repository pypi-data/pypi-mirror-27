

let getCellToFocus = function(nbCells, focus) {

	focus = parseInt(focus);
	focus = focus >= 0 ? focus : transformNegativeIndex(focus, nbCells);
	return focus;
};

let transformNegativeIndex = function(negIndex, nbCells) {
	return nbCells.length + negIndex;
};
