document.addEventListener('DOMContentLoaded', () => {
    // Debounce helper
    const debounce = (fn, delay = 300) => {
      let timer;
      return (...args) => {
        clearTimeout(timer);
        timer = setTimeout(() => fn(...args), delay);
      };
    };
  
    // Toggle comments via event delegation
    document.body.addEventListener('click', e => {
      if (e.target.matches('.toggle-comment, .toggle-comment *')) {
        const btn = e.target.closest('.toggle-comment');
        const id = btn.dataset.productId;
        const ta = document.querySelector(`textarea[data-product-id="${id}"]`);
        if (ta) ta.style.display = ta.style.display === 'block' ? 'none' : 'block';
      }
    });
  
    // Quantity input change => update cache & status
    document.body.addEventListener('input', e => {
      const input = e.target.closest('.quantity-input, input[name="quantity"]');
      if (input) {
        const id = input.dataset.productId || input.id.split('-')[1];
        window.productDataCaches ||= {};
        window.productDataCaches[id] ||= {};
        window.productDataCaches[id].quantity = input.value;
        const status = document.querySelector(`#status-${id}`);
        if (status) status.value = 'en_cours';
      }
    });
  
    // Event delegation for search inputs
    const searchFields = document.querySelectorAll('[id^="productSearch"]');
    searchFields.forEach(field => {
      const container = field.closest('form, .modal');
      const url = field.dataset.url;
      const targetClass = field.dataset.container;
      const fetchProducts = debounce(() => {
        fetch(`${url}?query=${field.value}`)
          .then(res => res.json())
          .then(data => renderProducts(data.products, targetClass))
          .catch(console.error);
      }, 300);
      field.addEventListener('input', fetchProducts);
    });
  
    // Shared product renderer
    function renderProducts(products, containerClass) {
      const container = document.querySelector(`.modal-body .row.${containerClass}`);
      if (!container) return;
      container.innerHTML = '';
      products.forEach(p => {
        const cached = window.productDataCaches[p.id] || { quantity: p.checklist_quantity || 0, comment: p.commentaire || '' };
        const qtyColor = p.quantity <= 0 ? 'red' : 'green';
        container.insertAdjacentHTML('beforeend', `
          <div class="col-12 product-item d-flex align-items-center justify-content-between">
            <h6 class="product-name mb-0 me-3">${p.name} <strong style="color:${qtyColor}">(${qtyColor=="red"?0:p.quantity})</strong></h6>
            <input type="number" class="form-control text-center quantity-input" data-product-id="${p.id}" value="${cached.quantity}" min="0" required>
            <button type="button" class="btn btn-secondary btn-sm toggle-comment" data-product-id="${p.id}">
              <i class="fa fa-comment-dots"></i>
            </button>
            <textarea class="form-control mt-2 comment-textarea" data-product-id="${p.id}" style="display:none;">${cached.comment}</textarea>
          </div>`);
      });
    }
  
    // Global popover init
    document.querySelectorAll('[data-bs-toggle="popover"]').forEach(el =>
      new bootstrap.Popover(el)
    );
  
    // Photo modal handlers
    window.openModal = function(imageUrl) {
      const m = document.getElementById("photoModal");
      document.getElementById("modalImg").src = imageUrl;
      document.getElementById("downloadBtn").href = imageUrl;
      m.style.display = "flex";
    };
    window.closeModal = () => document.getElementById("photoModal").style.display = "none";
  
    // PDF generation (factorisation des deux fonctions)
    window.generatePDF = type => {
      const modalBody = document.querySelector(`#verifier${type}Modal .modal-body-verif`);
      if (!modalBody) return alert("Contenu introuvable !");
      const { jsPDF } = window.jspdf;
      const pdf = new jsPDF({ orientation: 'portrait', unit: 'mm', format: 'a4' });
      const W = pdf.internal.pageSize.getWidth();
      const H = pdf.internal.pageSize.getHeight();
      let y = 10;
  
      // Header
      ['#checklistName', '#date', '#conseiller', '#numContrat'].forEach(sel => {
        pdf.setFontSize(sel === '#checklistName' ? 16 : 12);
        pdf.text(document.querySelector(sel).textContent.trim(), W / 2, y, { align: 'center' });
        y += sel === '#checklistName' ? 10 : 5;
      });
      y += 5;
  
      modalBody.cloneNode(true).querySelectorAll('.col-md-6').forEach(cat => {
        const rows = Array.from(cat.querySelectorAll('tr'));
        const data = rows.map(row => Array.from(row.querySelectorAll('td')).slice(0, type === 'b' ? 3 : 2).map(td => td.textContent.trim()));
        if (data.length === 0) return;
        const estH = (data.length + 1) * 10;
        if (y + 20 + estH > H) { pdf.addPage(); y = 10; }
        pdf.setFontSize(14);
        pdf.text(cat.querySelector('h5').textContent.trim(), W / 2, y, { align: 'center' });
        y += 10;
        pdf.autoTable({
          head: [type === 'b' ? ["Nom", "Qté", "Commentaire"] : ["Nom", "Qté"]],
          body: data,
          startY: y,
          theme: 'grid',
          styles: { font: 'Arial', halign: 'center', valign: 'middle' },
          headStyles: { fillColor: [200, 200, 200], textColor: 0, fontStyle: 'bold' },
          margin: { left: 30, right: 30 },
        });
        y = pdf.lastAutoTable.finalY + 10;
      });
      pdf.save(type === 'b' ? 'Verification-Breuvages.pdf' : 'Verification-Checklist.pdf');
    };
  
    // Optional: search filter for itemList
    (() => {
      const search = document.getElementById('searchItems');
      const categories = document.querySelectorAll('#itemList .category-group');
      if (!search) return;
  
      search.addEventListener('input', () => {
        const q = search.value.toLowerCase();
        categories.forEach(cat => {
          let any = false;
          cat.querySelectorAll('.item').forEach(item => {
            const nm = item.dataset.name.toLowerCase();
            const ok = nm.includes(q);
            item.style.display = ok ? '' : 'none';
            any ||= ok;
          });
          cat.style.display = any ? '' : 'none';
        });
      });
    })();
  
    // jQuery document form AJAX
    $('#documentForm').on('submit', function(e) {
      e.preventDefault();
      const data = new FormData(this);
      $.ajax({
        url: uploadDocumentUrl,
        type: 'POST',
        data,
        contentType: false,
        processData: false,
        success: () => (alert("Document téléchargé !"), location.reload()),
        error: () => alert("Erreur upload")
      });
    });
    $('.delete-doc').on('click', function() {
      if (confirm("Supprimer ?")) {
        $.post(`/delete_document/${$(this).data('id')}/`, {
          headers: { 'X-CSRFToken': getCSRFToken() }
        }).done(() => (alert("Supprimé"), location.reload()))
          .fail(() => alert("Erreur"));
      }
    });
  
  }); // DOMContentLoaded
  