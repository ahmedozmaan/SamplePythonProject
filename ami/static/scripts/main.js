var pluralize = function (word, count) {
    if (count === 1) {
        return word;
    }

    return word + 's';
};

var bulkSelectors = {
    'selectAll': '#select_all',
    'checkedItems': '.checkbox-item',
    'colheader': '.col-header',
    'selectedRow': 'warning',
    'updateScope': '#scope',
    'bulkActions': '#bulk_actions'
};

$(document).ready(function () {




    $('#serial_number').select2({
        theme: "bootstrap"
    });
    $('#phone_number').select2({
        theme: "bootstrap"
    });

    if(document.getElementById("myChart")) {
 
        var ctx = document.getElementById("myChart").getContext('2d');

        var myChart = new Chart(ctx, {
            type: 'pie',
            data: {
                datasets: [{
                    data: [10, 20, 30],
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(153, 102, 255, 0.2)',
                        'rgba(255, 159, 64, 0.2)'
                    ]
                }],
                // These labels appear in the legend and in the tooltips when hovering different arcs
                labels: [
                    'Red',
                    'Yellow',
                    'Blue'
                ]
            }
        });
    }



    //data read
    var csrfToken = $('meta[name=csrf-token]').attr('content');
    $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
        var target = $(e.target).attr("href"); // activated tab
        var $tab;
        if (target === "#demand") {
            target = 0;
            $tab = $("#demandtb")
        } else if (target === "#alerts") {
            target = 1;
            $tab = $('#alertstb')
        } else if (target === "#hourly") {
            target = 2;
            $tab = $("#hourlytb")
        } else if (target === "#daily") {
            target = 3;
            $tab = $("#dailytb")
        } else if (target === "#monthly") {
            target = 4;
            $tab = $("#monthlytb")
        }
        getMeterData(csrfToken, target, $tab)

    });
    var $start = $("#start");
    var $end = $("#end");

    if ($start.length) {
        $start.datetimepicker({
            format: 'YYYY-MM-DD HH:mm:ss',
            icons: {
                time: 'fa fa-clock-o',
                date: 'fa fa-calendar',
                up: 'fa fa-arrow-up',
                down: 'fa fa-arrow-down',
                previous: 'fa fa-chevron-left',
                next: 'fa fa-chevron-right',
                clear: 'fa fa-trash'
            }
        });
    }

    if ($end.length) {
        $end.datetimepicker({
            format: 'YYYY-MM-DD HH:mm:ss',
            icons: {
                time: 'fa fa-clock-o',
                date: 'fa fa-calendar',
                up: 'fa fa-arrow-up',
                down: 'fa fa-arrow-down',
                previous: 'fa fa-chevron-left',
                next: 'fa fa-chevron-right',
                clear: 'fa fa-trash'
            }
        });
    }

    // Date formatting with momentjs.
    $('.from-now').each(function (i, e) {
        (function updateTime() {
            var time = moment($(e).data('datetime'));
            $(e).text(time.fromNow());
            $(e).attr('title', time.format('MMMM Do YYYY, h:mm:ss a Z'));
            setTimeout(updateTime, 1000);
        })();
    });

    $('.short-date').each(function (i, e) {
        var time = moment($(e).data('datetime'));
        $(e).text(time.format('MMM Do YYYY'));
        $(e).attr('title', time.format('MMMM Do YYYY, h:mm:ss a Z'));
    });

    // Bulk delete.
    $('body').on('change', bulkSelectors.checkedItems, function () {
        var checkedSelector = bulkSelectors.checkedItems + ':checked';
        var itemCount = $(checkedSelector).length;
        var pluralizeItem = pluralize('item', itemCount);
        var scopeOptionText = itemCount + ' selected ' + pluralizeItem;

        if ($(this).is(':checked')) {
            $(this).closest('tr').addClass(bulkSelectors.selectedRow);

            $(bulkSelectors.colheader).hide();
            $(bulkSelectors.bulkActions).show();
        }
        else {
            $(this).closest('tr').removeClass(bulkSelectors.selectedRow);

            if (itemCount === 0) {
                $(bulkSelectors.bulkActions).hide();
                $(bulkSelectors.colheader).show();
            }
        }

        $(bulkSelectors.updateScope + ' option:first').text(scopeOptionText);
    });

    $('body').on('change', bulkSelectors.selectAll, function () {
        var checkedStatus = this.checked;

        $(bulkSelectors.checkedItems).each(function () {
            $(this).prop('checked', checkedStatus);
            $(this).trigger('change');
        });
    });
});


function getMeterData(csrfToken, dataType, $tab) {
    //https://stackoverflow.com/questions/4758103/last-segment-of-url
    var id = window.location.href.substr(window.location.href.lastIndexOf('/') + 1);
    $.ajax({
        data: {dataType: dataType},
        type: 'POST',
        url: '/admin/meters/data/' + id,
        beforeSend: function (xhr) {
            xhr.setRequestHeader('X-CSRFToken', csrfToken);
        }
    }).done(function (data, status, xhr) {
        var tr = [];
        for (var i = 0; i < data.length; i++) {
            tr.push('<tr>');
            tr.push("<td>" + moment(data[i].capture_time).format('YYYY-MM-DD h:mm:ss') + "</td>");
            tr.push("<td>" + data[i].name + "</td>");
            tr.push("<td>" + data[i].code + "</td>");
            tr.push('</tr>');
        }
        var colCount = 0;
        $tab.find('tr:first th').each(function () {
            if ($(this).attr('colspan')) {
                colCount += +$(this).attr('colspan');
            } else {
                colCount++;
            }
        });
        tr.push('<tr>');
        tr.push("<td colspan=" + colCount + " align='center'> <a href='/admin/data/alert'>Show More</a> </td>");
        tr.push('</tr>');

        $tab.children().eq(1).children().remove();
        $tab.append($(tr.join('')));

    }).fail(function (xhr, status, error) {
        console.log("fail ");
        console.log("csrfToken " + csrfToken);
        console.log("dataType  " + dataType);
        console.log("status  " + status);
        console.log("error  " + error);
        var colCount = 0;
        $tab.find('tr:first th').each(function () {
            if ($(this).attr('colspan')) {
                colCount += +$(this).attr('colspan');
            } else {
                colCount++;
            }
        });

        var tr = [];
        tr.push('<tr>');
        tr.push("<td colspan=" + colCount + " align='center'> <a href='/admin/data/alert'>No Data Found</a> </td>");
        tr.push('</tr>');

        $tab.children().eq(1).children().remove();
        $tab.append($(tr.join('')));

    }).always(function (xhr, status, error) {
        console.log("csrfToken " + csrfToken);
        console.log("dataType  " + dataType);
        console.log("status  " + status);
        console.log("error  " + error);

    });
}

