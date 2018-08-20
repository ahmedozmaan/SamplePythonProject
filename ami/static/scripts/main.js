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
        var links;
        if (target === "#demand") {
            target = 0;
            $tab = $("#demandtb")
            links="demand"
        } else if (target === "#alerts") {
            target = 1;
            $tab = $('#alertstb')
            links="alert"
        } else if (target === "#hourly") {
            target = 2;
            $tab = $("#hourlytb")
            links="hourly"
        } else if (target === "#daily") {
            target = 3;
            $tab = $("#dailytb")
            links="daily"
        } else if (target === "#monthly") {
            target = 4;
            $tab = $("#monthlytb")
            links="monthly"
        }
        getMeterData(csrfToken, target, $tab,links)

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


function getMeterData(csrfToken, dataType, $tab,links) {
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
        if(dataType==1){
          for (var i = 0; i < data.length; i++) {
              tr.push('<tr>');
              tr.push("<td>" + moment(data[i].capture_time).format('YYYY-MM-DD h:mm:ss') + "</td>");
              tr.push("<td>" + data[i].name + "</td>");
              tr.push("<td>" + data[i].code + "</td>");
              tr.push('</tr>');
              id = data[i].sequence_number
          }
        } else if(dataType==2)
        {
            for (var i = 0; i < data.length; i++)
            {
                tr.push('<tr>');
                tr.push("<td>" + moment(data[i].capture_time).format('YYYY-MM-DD h:mm:ss') + "</td>");
                tr.push("<td>" + data[i].import_active + "</td>");
                tr.push("<td>" + data[i].export_active + "</td>");
                tr.push("<td>" + data[i].import_reactive + "</td>");
                tr.push("<td>" + data[i].export_reactive+ "</td>");
                tr.push("<td>" + data[i].import_apparent + "</td>");
                tr.push("<td>" + data[i].export_apparent+ "</td>");
                tr.push('</tr>');
                id = data[i].sequence_number
            }
        } else if(dataType==3)
        {
          for (var i = 0; i < data.length; i++)
          {
              tr.push('<tr>');
              tr.push("<td>" + moment(data[i].capture_time).format('YYYY-MM-DD h:mm:ss') + "</td>");
              tr.push("<td>" + data[i].active_increase + "</td>");
              tr.push("<td>" + data[i].total_active + "</td>");
              tr.push("<td>" + data[i].import_active + "</td>");
              tr.push("<td>" + data[i].export_active+ "</td>");
              tr.push('</tr>');
              id = data[i].sequence_number
          }
        } else if(dataType==4)
        {
          for (var i = 0; i < data.length; i++)
          {
              tr.push('<tr>');
              tr.push("<td>" + moment(data[i].capture_time).format('YYYY-MM-DD h:mm:ss') + "</td>");
              tr.push("<td>" + data[i].active_increase + "</td>");
              tr.push("<td>" + data[i].total_active + "</td>");
              tr.push("<td>" + data[i].import_active + "</td>");
              tr.push("<td>" + data[i].export_active + "</td>");
              tr.push("<td>" + data[i].import_reactive + "</td>");
              tr.push("<td>" + data[i].export_reactive+ "</td>");
              tr.push("<td>" + data[i].import_apparent + "</td>");
              tr.push("<td>" + data[i].export_apparent+ "</td>");
              tr.push('</tr>');
              id = data[i].sequence_number
          }
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
        tr.push("<td colspan=" + colCount + " align='center'> <a href='/admin/data/"+links+"?q="+id+"'>Show More</a> </td>");
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
        tr.push("<td colspan=" + colCount + " align='center'> <a href='/admin/data/"+links+">No Data Found</a> </td>");
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
