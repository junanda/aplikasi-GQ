let dataResponse;
let dataDistance;
let p_detail = $("#now-step");
let valK;

$("#excelFile").change(function () {
    $("#load").prop("disabled", false);
})

$("#load").on("click", function () {
    var form_data = new FormData();
    form_data.append('file', $("#excelFile").prop('files')[0])
    $.ajax({
        url: `${urlit}load-file`,
        dataType: 'json',
        contentType: false,
        processData: false,
        data: form_data,
        type: 'post',
        success: function (response) {
            // console.info(response.data);
            dataResponse = response.data
            var dataBody = '';
            $.each(dataResponse, function (key, data) {
                dataBody += `<tr>
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

            $("#data-list tr").replaceWith(dataBody);
            $("#excelFile").val("")
            $("#excelFile").prop('disabled', true);
            $("#load").prop('disabled', true);
            $("#btn-next").removeAttr("hidden");
            p_detail.text("Data Excel berhasil di load...");
            $("#sel-k").removeAttr("hidden")
        },
        error: function (response) {
            $("#msg").html(response.message);
        }
    });

    $("#btn-next").click(function () {
        let now_step = $(this).attr('data-next');
        let next_step;
        switch (now_step) {
            case 'distance':
                next_step = 'sorting';
                break;
            case 'sorting':
                next_step = 'neighbors';
                break;
            case 'neighbors':
                next_step = 'label';
                break;
            case 'label':
                next_step = 'finish';
                break;
        }

        if (now_step !== 'label') {
            $(this).text(`Next ${next_step}`);
            $(this).attr('data-next', next_step);
        } else {
            $(this).prop('disabled', true);
            $(this).text('Finish');
        }

        console.log(now_step, next_step);
        if (now_step === 'distance') {
            $.ajax({
                url: `${urlit}calculate`,
                dataType: 'json',
                contentType: 'application/json',
                data: JSON.stringify({ 'step': now_step, 'data': dataResponse }),
                type: 'post',
                success: function (res) {
                    dataDistance = res.data
                    let th_new = '<tr><th>No</th><th widht="30%">Nama</th>';
                    let tr_new = '';

                    // console.info(dataDistance[0].detail.length)
                    $.each(dataDistance[0].detail, function (key, val) {
                        th_new += `<th>${val.dokumen}</th>`;
                    });
                    th_new += '</tr>';
                    $("#tabledata thead").html(th_new);
                    $("#tabledata tfoot").html(th_new);

                    $.each(dataDistance, function (key, data) {
                        tr_new += `<tr>
                                    <td>${key + 1}</td>
                                    <td>${data.nama}</td>`;

                        $.each(data.detail, function (kk, val) {
                            tr_new += `
                                    <td>${val.distance}</td>
                                `;
                        })
                        tr_new += `</tr>`;
                    })
                    p_detail.text(res.informasi)
                    $("#data-list").html(tr_new)
                }
            })
        } else if (now_step === 'sorting') {
            let th_new = '<tr><th>No</th><th widht="30%">Nama</th>';
            let tr_new = '';
            let i = 1;

            $.each(dataDistance[0].detail, function (key, val) {
                th_new += `<th colspan="2"># Ketetanggaan Terdekat ${key + 1}</th><th>Label</th>`;
            });

            $("#tabledata thead").html(th_new);
            $("#tabledata tfoot").html(th_new);

            $.each(dataDistance, function (key, val) {
                val.detail.sort((a, b) => {
                    return a.distance - b.distance;
                });
            })

            dataDistance.forEach((e) => {
                tr_new += `<tr>
                            <td>${i}</td>
                            <td>${e.nama}</td>
                        `;
                e.detail.forEach((data) => {
                    // console.log(`nama: ${e.nama} dokumen : ${data.dokumen}`);
                    tr_new += `<td class="table-info">${data.dokumen}</td><td>${data.distance}</td><td class="table-warning">${data.label}</td>`;
                })

                tr_new += '</tr>';
                i++;
            })

            p_detail.text("Hasil Sorting jarak terdekat...")
            $("#data-list").html(tr_new);
        } else if (now_step === 'neighbors') {
            const k_val = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
            p_detail.text("Pilih Jumlah Ketetangaan terdekat...")
            $("#tetangga").prop('disabled', false);

            let optHtml = '';
            k_val.forEach((val) => {
                optHtml += `<option value="${val}">${val}</option>`;
            });

            $("#tetangga").html(optHtml);

        } else if (now_step === 'label') {
            $("#tetangga").prop('disabled', true);
            calculateLabelData();
        }

    });

    $("#tetangga").change(function () {
        valK = $(this).val();
    });

    function calculateLabelData() {
        let classL = []
        let loop = { labelP0: 0, labelP1: 0 };
        let th_html = '';
        let tr_html = '';
        $.each(dataDistance, (key, val) => {
            ;
            $.each(val.detail, (i, data) => {
                if (i >= valK) {
                    return true;
                }

                if (data.label === '0') {
                    loop.labelP0 += 1;
                } else {
                    loop.labelP1 += 1;
                }
            })

            classL.push({ class1: loop.labelP0, class2: loop.labelP1 });
            loop.labelP0 = 0;
            loop.labelP1 = 0;
        })
        th_html += `<tr>
                    <th>No</th>
                    <th>Nama</th>
                    <th>Nilai SKP</th>
                    <th>Orientasi</th>
                    <th>Integritas</th>
                    <th>Komitmen</th>
                    <th>Disiplin</th>
                    <th>Kerjasama</th>
                    <th>Label Data</th>
                </tr>`;
        $.each(dataResponse, function (key, val) {
            tr_html += `<tr>
                        <td>${key + 1}</td>
                        <td>${val.nama}</td>
                        <td>${val.nilai_skp}</td>
                        <td>${val.orientasi}</td>
                        <td>${val.integritas}</td>
                        <td>${val.komitmen}</td>
                        <td>${val.disiplin}</td>
                        <td>${val.kerjasama}</td>`;
            (classL[key].class1 > classL[key].class2) ? tr_html += '<td class="table-primary">0</td>' : tr_html += '<td class="table-info">1</td>';
            tr_html += '</tr>';
        });

        $("#tabledata thead").html(th_html);
        $("#data-list").html(tr_html);
        $("#tabledata tfoot").html(th_html);
        p_detail.text("Hasil pelabelan data");
    }
})