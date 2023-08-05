
"use strict";

console.log('start main');

require([
	'jquery',
	'base/js/dialog',
	'base/js/events',
	'base/js/namespace',
	'notebook/js/celltoolbar',
	'notebook/js/codecell',
	'base/js/promises'
], function (
	$,
	dialog,
	events,
	Jupyter,
	celltoolbar,
	codecell,
	promises
) {
		events.on('kernel_ready.Kernel', function () {
			console.log('start autorun');
			if (Jupyter.notebook.trusted) {
				// notebook is trusted js can run
				console.log('notebook is trusted');
				let nbCells = Jupyter.notebook.get_cells(),
					arrCells;
				window.debugNbCells = nbCells;

				{% if data.str_cells is defined and data.str_cells != None and data.str_cells != '' %}
				{% include 'getCellsFromString.js' %}
				console.log('str_cells=' + '__$data.str_cells$__');
				arrCells = getCellsFromString('__$data.str_cells$__', nbCells);
				{% endif %}

				{% if data.metadata is defined and data.metadata %}
				{% include 'getCellsFromMetadata.js' %}
				arrCells = getCellsFromMetadata(nbCells);
				{% endif %}

				{% if data.comment is defined and data.comment %}
				{% include 'getCellsFromComment.js' %}
				arrCells = getCellsFromComment(nbCells, '__$data.comment_flag$__');
				{% endif %}

				console.log(arrCells);
				for (let i of arrCells) {
					let nbCell = nbCells[i];
					if (nbCell) {
						console.log('execute cell ' + i);
						nbCell.execute();
					}
					else {
						console.log('cell ' + i + ' does not exist');
					}
				}

				{% if data.focus is defined %}
				{% include 'getCellToFocus.js' %}
				let f = getCellToFocus(nbCells, '__$data.focus$__');
				let nbCell = nbCells[f];
				if (nbCell) {
					console.log('focus on cell ' + f);
					nbCell.focus_cell();
				}
				else {
					console.log('cell ' + f + ' does not exist');
				}
				{% endif %}

			}
			else {
				// notebook is not trusted let the user know about it
				// by definition this should never happen as
				// js cannot run if notebook not trustee
				console.log('notebook is not trusted');
				console.log('nothing is done');
			}
		});




	});

console.log('end main');
