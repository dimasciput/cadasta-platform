function setup_filter(document, $) {
    'use strict';

    $(document).on('init.dt', function (e, dtSettings) {
        if (e.namespace !== 'dt') {
            return;
        }
        var addSelectOptions = function () {
            var aData = ['Active', 'Archived', 'All'];
            var r = '<label><select class="form-control input-sm" id="archive-filter">', i, iLen = aData.length;
            for (i = 0; i < iLen; i += 1) {
                r += '<option value="' + aData[i] + '">' + aData[i] + '</option>';
            }
            return r + '</select></label>';
        };

        var table = $('#DataTables_Table_0').DataTable();
        if ($(".unarchived").length) {
            table.order([1, 'asc']).draw();
        }

        if ($(".archived").length) {
            dtSettings.nTableWrapper.childNodes[0].childNodes[0].innerHTML += addSelectOptions();
            table.columns(0).search('False').draw();

            $('input').on('keyup', function () {
                table.search(this.value).draw();
            });

            $('#archive-filter').change(function () {
                var value = '';
                table.search(value).draw();
                var selection = $('#archive-filter').val();
                if (selection === 'Active') {
                    value = 'False';
                } else if (selection === 'Archived') {
                    value = 'True';
                }
                table.columns(0).search(value).draw();
            });
        }
    });
}

setup_filter(document, jQuery);


function setup_search_filter(document, $) {
    'use strict';

    $(document).on('init.dt', function (e, dtSettings) {
        if (e.namespace !== 'dt') {
            return;
        }
        var addSelectOptions = function () {
            var aData = ['Show all', 'Show only locations', 'Show only relationships', 'Show only parties', 'Show only resources'];
            var r = '<label><select class="form-control input-sm" id="entity-type-filter">', i, iLen = aData.length;
            for (i = 0; i < iLen; i += 1) {
                r += '<option value="' + aData[i] + '">' + aData[i] + '</option>';
            }
            return r + '</select></label>';
        };

        var table = $('#search-results').DataTable();
        if ($(".entity-type").length) {
            table.order([1, 'asc']).draw();
        }

        if ($(".entity-type").length) {
            dtSettings.nTableWrapper.childNodes[0].childNodes[0].innerHTML += addSelectOptions();
        }

        $('#entity-type-filter').change(function () {
            var value = '';
            table.search(value).draw();
            var selection = $('#entity-type-filter').val();
            if (selection === 'Show only locations') {
                value = 'Location';
            } else if (selection === 'Show only relationships') {
                value = 'Relationship';
            } else if (selection === 'Show only parties') {
                value = 'Party';
            } else if (selection === 'Show only resources') {
                value = 'Resource';
            }
            table.columns(0).search(value).draw();
        });
    });
}

setup_search_filter(document, jQuery);