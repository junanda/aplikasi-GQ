let dataExcel;
let dataExlabel;
let p_info = $("#now-step")
// let btnNext = `<button class="btn btn-primary" id="btn-next" data-next="calculate">Calculate distance</button>`
$("#file").change(function () {
    $("#import").prop("disabled", false);
})

$("#import").on("click", function () {
    var form_data = new FormData();
    form_data.append('file', $("#file").prop('files')[0])
    $.ajax({
        url: `${url}file-excel`,
        dataType: 'json',
        contentType: false,
        processData: false,
        data: form_data,
        type: 'post',
        success: function (response) {
            dataExcel = response.data
            var html = '';
            $.each(dataExcel, function (key, data) {
                html += `<tr>
                            <td>${data.no}</td>
                            <td>${data.nama}</td>
                            <td>${data.nilai_skp}</td>
                            <td>${data.orientasi}</td>
                            <td>${data.integritas}</td>
                            <td>${data.komitmen}</td>
                            <td>${data.disiplin}</td>
                            <td>${data.kerjasama}</td>
                        </tr>`;
            })
            $("#list-data tr").replaceWith(html);
            $("#file").val("")
            $("#import").prop("disabled", true);
            $("#btn-next").removeAttr("hidden");
            $("#file").prop('disabled', true);
            p_info.text("Data Excel berhasil di load....")
        },
        error: function (response) {
            $("#msg").html(response.message);
        }
    })
})

$("#btn-next").click(function () {
    let now_step = $(this).attr('data-next');
    let next_step;

    switch (now_step) {
        case 'centroid_1':
            next_step = 'centroid_2';
            break;
        case 'centroid_2':
            next_step = 'distance';
            break;
        case 'distance':
            next_step = 'label';
            break;
        case 'label':
            next_step = 'save'
            break;
        case 'save':
            next_step = 'finish'
    }
    if (now_step !== 'save') {
        $(this).text(`Next ${next_step}`);
        $(this).attr("data-next", next_step);
    } else {
        $(this).prop('disabled', true);
        $(this).text("Finish");
    }

    if (now_step === 'label') {
        $(".table thead tr").append('<th>Label</th>');
        $(".table tfoot tr").append('<th>Label</th>');
        let row = ''
        $.each(dataExlabel, function (key, data) {
            row += '<tr>';
            row += `<td>${data.no}</td>
                        <td>${data.nama}</td>
                        <td>${data.nilai_skp}</td>
                        <td>${data.orientasi}</td>
                        <td>${data.integritas}</td>
                        <td>${data.komitmen}</td>
                        <td>${data.disiplin}</td>
                        <td>${data.kerjasama}</td>
                        <td class="table-info">${data.jarak_centroid_0}</td>
                        <td class="table-primary">${data.jarak_centroid_1}</td>`
            if (data.jarak_centroid_0 < data.jarak_centroid_1) {
                row += '<td class="table-success">Cluster 1 </td>';
            } else {
                row += '<td class="table-danger">Cluster 2 </td>'
            }
            row += '</tr>';
        });

        $("#list-data").html(row);
        p_info.text("Proses Akhir pada K-Means Clustering");
        
    } else if(now_step === 'save'){
        $.ajax({
            url: `${url}save-calculate`,
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify({'data': dataExlabel}),
            type: 'post',
            success: function (res) {
                alert(res['informasi']);
                location.reload();
            }
        })
    } else {
        $.ajax({
            url: `${url}calculate`,
            dataType: 'json',
            contentType: "application/json",
            data: JSON.stringify({ 'step': now_step, 'data': dataExcel }),
            type: 'post',
            success: function (res) {
                let data_res = res.data;
                var tr_new = '';

                $.each(data_res, function (key, data) {
                    if (now_step === 'distance') {
                        tr_new += `<tr>
                                <td>${data.no}</td>
                                <td>${data.nama}</td>
                                <td>${data.nilai_skp}</td>
                                <td>${data.orientasi}</td>
                                <td>${data.integritas}</td>
                                <td>${data.komitmen}</td>
                                <td>${data.disiplin}</td>
                                <td>${data.kerjasama}</td>
                                <td class="table-info">${data.jarak_centroid_0}</td>
                                <td class="table-primary">${data.jarak_centroid_1}</td>
                            </tr>`;
                    } else {
                        tr_new += `<tr>
                                <td>${data.no}</td>
                                <td>${data.nama}</td>
                                <td>${data.nilai_skp}</td>
                                <td>${data.orientasi}</td>
                                <td>${data.integritas}</td>
                                <td>${data.komitmen}</td>
                                <td>${data.disiplin}</td>
                                <td>${data.kerjasama}</td>
                            </tr>`;
                    }
                })

                if (now_step === 'distance') {
                    addeHeadAndBodyCol();
                    dataExlabel = data_res;
                }
                // tr_new += "</tbody>"; 
                $("#list-data").html(tr_new);
                p_info.text(res.informasi)
            },
            error: function (res) {
                console.error(res.message);
            }
        });
    }
})

function addeHeadAndBodyCol() {
    let th = `<th>Jarak centroid 0</th>
                    <th>Jarak centroid 1</th>`;
    $(".table thead tr").append(th);
    $(".table tfoot tr").append(th);
}