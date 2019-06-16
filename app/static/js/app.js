let IPDataTableModels = {
    tableObj: null
};
let IPDataTableControllers = {
    initIPDataTable: () => {
        let IPDataTable = $("#IPDataTable");
        //noinspection JSUnresolvedFunction
        let IPDataTableObj = IPDataTable.DataTable({
            processing: true,
            serverSide: true,
            ajax: {
                "url": `/ip_query_datatable/datastream`,
            },
            orderCellsTop: true,
            columns: [
                {title: "IP"},
                {title: "Country Code"},
                {title: "Region Code"},
                {title: "City"},
                {title: "Zip"},
                {title: "Latitude"},
                {title: "Longitude"},
                {title: "Registrant Handle"},
                {title: "Registrant Description"},
                {title: "RDAP Type"}
            ],
            dom: "lfrtip",
            order: [[0, "asc"]]
        });
        IPDataTableObj.buttons().container().appendTo($(".col-sm-6:eq(0)", IPDataTableObj.table().container()));
        initDataTable(IPDataTableObj, IPDataTable);
        IPDataTableModels.tableObj = IPDataTableObj;
    }
};

/**
 * Setup for all DataTables.
 * @param table
 * @param datatable
 */
function initDataTable(table, datatable) {
    // Setup - add a text input to each header cell
    datatable.find("thead th").each(function (i) {
        let title = datatable.find("thead th").eq($(this).index()).text();
        if (title !== "Actions" && title !== "Add" && title !== "Edit" && title !== "Delete" && title !== "Select") {
            $(this).html(`${title}<br><input type="text" onclick="stopPropagation(event);" data-index="${i}" />`);
        }
    });

    // Filter event handler
    $(table.table().container()).on("keyup", "thead input", function () {
        //noinspection JSUnresolvedFunction
        table.column($(this).data("index")).search(this.value).draw();
    });
}

/**
 * Stops events from bubbling past a certain event.
 * @param event
 */
function stopPropagation(event) {
    if (event.stopPropagation !== undefined) {
        event.stopPropagation();
    } else {
        event.cancelBubble = true;
    }
}