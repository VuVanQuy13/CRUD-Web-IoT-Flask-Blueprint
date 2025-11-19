const API_farm = "http://192.168.1.6:2004/board/";


const btnAdd = document.getElementById('btnAdd') 
const nameInput = document.getElementById('namefarm')
const descInput = document.getElementById('description')
const farmTable = document.getElementById('farmTable').querySelector('tbody')

document.addEventListener("DOMContentLoaded" , () => {
    // Thêm
    btnAdd.addEventListener('click' , async() => {
        const name = nameInput.value.trim()
        const desc = descInput.value.trim()
        if (!name) {
            return alert('Tên farm bắt buộc phải có')
        }

        try {
            const res = await fetch(API_farm + "/api/add" , {
                method: "POST",
                headers: {"Content-Type" : "application/json"},
                body: JSON.stringify({
                    "namefarm": name,
                    'description':desc
                })
            })

            const data = await res.json()

            if (data.error) {
                return alert(data.error)
            }

            const tr = document.createElement("tr")
            tr.dataset.id = data.id
            tr.innerHTML = `
                <td>${data.id}</td>
                <td class="farm-name">${data.namefarm}</td>
                <td class="farm-desc">${data.description}</td>
                <td>
                    <button class="btn btn-warning btn-sm btn-edit">Sửa</button>
                    <button class="btn btn-danger btn-sm btn-delete">Xóa</button>
                    <button class="btn btn-primary btn-sm btn-select">Chọn</button>
                </td>
            `
            farmTable.appendChild(tr)
            nameInput.value = ''
            descInput.value = ''
        } catch (err) {
            alert("Lỗi khi thêm farm: " + err.message)
        }

    })

    farmTable.addEventListener('click' , async e => {
        const tr = e.target.closest('tr')
        if(!tr) return

        const id = tr.dataset.id

        // DELETE farm
        if(e.target.classList.contains('btn-delete')) {
            if (!confirm('Bạn có chắc muốn xóa form này?')) return

            try {
                await fetch( API_farm + `/api/delete/${id}` , {method: "DELETE"})
                tr.remove()
            } catch(err) {
                alert("Lỗi khi xóa farm" + err.message)
            }
        }

        // Update farm
        else if (e.target.classList.contains('btn-edit')) {
            const oldName = tr.querySelector('.farm-name').innerText
            const oldDesc = tr.querySelector('.farm-desc').innerText

            const editTr = document.createElement('tr')
            editTr.classList.add('edit-row')
            editTr.innerHTML = `
                <td colspan="4">
                <div class="d-flex gap-2">
                    <input type="text" class="form-control form-control-sm edit-name" value="${oldName}" placeholder="Tên farm">
                    <input type="text" class="form-control form-control-sm edit-desc" value="${oldDesc}" placeholder="Mô tả">
                    <button class="btn btn-success btn-sm btn-save">Lưu</button>
                    <button class="btn btn-secondary btn-sm btn-cancel">Hủy</button>
                </div>
                </td>
            `
            // Chèn form sửa ngay sau hàng hiện tại muốn sửa
            tr.after(editTr)

            editTr.querySelector('.btn-cancel').addEventListener('click', () =>  {
                editTr.remove()
            })

            editTr.querySelector('.btn-save').addEventListener('click' , async () => {
                const newName = editTr.querySelector('.edit-name').value.trim()
                const newDesc = editTr.querySelector('.edit-desc').value.trim()

                if(!newName) {
                    return alert('Tên Farm không được để trống!')
                }

                try {
                    await fetch(API_farm + `/api/update/${id}` , {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({
                            "namefarm": newName,
                            "description": newDesc
                        })
                    })
    
                    tr.querySelector('.farm-name').innerText = newName
                    tr.querySelector('.farm-desc').innerText = newDesc
                    
                    editTr.remove()
                } catch (err) {
                    alert("Lỗi khi cập nhật farm: " + err.message);
                }
            })
        }

        // SELECT farm
        else if(e.target.classList.contains('btn-select')) {
            window.location.href = `/farm/${id}`
        }



    })
})