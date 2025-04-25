
// Function to bind comment toggle events
function bindCommentToggleEvents() {
    document.querySelectorAll('.toggle-comment').forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.getAttribute("data-product-id");
            const targetTextarea = document.querySelector(`textarea[data-product-id='${productId}']`);
            
            if (targetTextarea) {
                // Toggle the display of the textarea
                targetTextarea.style.display = (targetTextarea.style.display === "none" || targetTextarea.style.display === "") ? "block" : "none";
            }
        });
    });
}

// Call the function when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    bindCommentToggleEvents();
});

async function generatePDFb() {
    const { jsPDF } = window.jspdf;

    // Select dynamic data
    const checklistName = document.querySelector('#checklistName').textContent.trim();
    const date = document.querySelector('#date').textContent.trim();
    const conseiller = document.querySelector('#conseiller').textContent.trim();
    const numContrat = document.querySelector('#numContrat').textContent.trim();

    const modalContent = document.querySelector('#verifierbModal .modal-body-verif');
    if (!modalContent) {
        alert("Le contenu de la modal est introuvable !");
        return;
    }
    const clonedContent = modalContent.cloneNode(true);

    const categories = clonedContent.querySelectorAll('.col-md-6');
    const validCategories = Array.from(categories).filter(category => {
        const rows = category.querySelectorAll('tr');
        let hasValidItems = false;

        rows.forEach(row => {
            const quantityCell = row.children[1];
            const commentaireCell = row.children[2]?.querySelector('i')?.getAttribute('data-bs-content') || '';

            // Retain row if quantity > 0 or there is a commentaire
            if ((quantityCell && parseInt(quantityCell.textContent.trim()) > 0) || commentaireCell) {
                hasValidItems = true;
            } else {
                row.remove(); // Remove rows with no quantity and no commentaire
            }
        });

        if (!hasValidItems) {
            category.remove();
        }

        return hasValidItems;
    });

    if (validCategories.length === 0) {
        alert("Aucune catégorie valide pour le PDF !");
        return;
    }

    const pdf = new jsPDF({
        orientation: 'portrait',
        unit: 'mm',
        format: 'a4',
    });

    const pageWidth = pdf.internal.pageSize.getWidth();
    const pageHeight = pdf.internal.pageSize.getHeight();
    let cursorY = 10;

    // Add header
    pdf.setFont("Arial", "bold");
    pdf.setFontSize(16);
    pdf.text(`Breuvage pour ${checklistName}`, pageWidth / 2, cursorY, { align: "center" });
    cursorY += 10;
    pdf.setFontSize(12);
    pdf.text(`${date}`, pageWidth / 2, cursorY, { align: "center" });
    cursorY += 5;
    pdf.text(`${conseiller}`, pageWidth / 2, cursorY, { align: "center" });
    cursorY += 5;
    pdf.text(`${numContrat}`, pageWidth / 2, cursorY, { align: "center" });
    cursorY += 10;

    validCategories.forEach(category => {
        const categoryName = category.querySelector('h5').textContent.trim();
        const rows = category.querySelectorAll('tr');
        const headers = ["Nom de l'article", "Quantité","Commentaire","Consommé","Restant"];
        const data = Array.from(rows).map(row => {
            const cells = row.querySelectorAll('td');
            const commentaire = cells[2]?.querySelector('i')?.getAttribute('data-bs-content') || '';
            return [
                cells[0]?.textContent.trim() || '', // Item Name
                cells[1]?.textContent.trim() || '', // Quantity
                commentaire // Commentaire
            ];
        });

        // Estimate table height
        const estimatedTableHeight = (data.length + 1) * 10; // Approx 10mm per row including header

        // Check if the table fits on the current page
        if (cursorY + 20 + estimatedTableHeight > pageHeight) {
            pdf.addPage();
            cursorY = 10;
        }

        // Add category name
        pdf.setFontSize(14);
        pdf.text(categoryName, pageWidth / 2, cursorY, { align: "center" });
        cursorY += 10;

        // Add table
        pdf.autoTable({
            head: [headers],
            body: data,
            startY: cursorY,
            theme: 'grid',
            styles: {
                font: 'Arial',
                halign: 'center',
                valign: 'middle',
            },
            headStyles: {
                fillColor: [200, 200, 200],
                textColor: 0,
                fontStyle: 'bold',
            },
            margin: { left: 30, right: 30 },
        });

        cursorY = pdf.lastAutoTable.finalY + 10; // Update cursorY
    });

    pdf.save('Verification-Breuvages.pdf');
}



async function generatePDF() {
    const { jsPDF } = window.jspdf;

    // Select dynamic data
    const checklistName = document.querySelector('#checklistName').textContent.trim();
    const date = document.querySelector('#date').textContent.trim();
    const conseiller = document.querySelector('#conseiller').textContent.trim();
    const numContrat = document.querySelector('#numContrat').textContent.trim();

    const modalContent = document.querySelector('#verifierModal .modal-body-verif');
    if (!modalContent) {
        alert("Le contenu de la modal est introuvable !");
        return;
    }
    const clonedContent = modalContent.cloneNode(true);

    const categories = clonedContent.querySelectorAll('.col-md-6');
    const validCategories = Array.from(categories).filter(category => {
        const rows = category.querySelectorAll('tr');
        let hasValidItems = false;

        rows.forEach(row => {
            const quantityCell = row.children[1];
            if (quantityCell && parseInt(quantityCell.textContent.trim()) > 0) {
                hasValidItems = true;
            } else {
                row.remove(); // Remove rows with quantity = 0
            }
        });

        if (!hasValidItems) {
            category.remove();
        }

        return hasValidItems;
    });

    if (validCategories.length === 0) {
        alert("Aucune catégorie valide pour le PDF !");
        return;
    }

    const pdf = new jsPDF({
        orientation: 'portrait',
        unit: 'mm',
        format: 'a4',
    });

    const pageWidth = pdf.internal.pageSize.getWidth();
    const pageHeight = pdf.internal.pageSize.getHeight();
    let cursorY = 10;

    // Add header
    pdf.setFont("Arial", "bold");
    pdf.setFontSize(16);
    pdf.text(`${checklistName}`, pageWidth / 2, cursorY, { align: "center" });
    cursorY += 10;
    pdf.setFontSize(12);
    pdf.text(`${date}`, pageWidth / 2, cursorY, { align: "center" });
    cursorY += 5;
    pdf.text(`${conseiller}`, pageWidth / 2, cursorY, { align: "center" });
    cursorY += 5;
    pdf.text(`${numContrat}`, pageWidth / 2, cursorY, { align: "center" });
    cursorY += 10;

    validCategories.forEach(category => {
        const categoryName = category.querySelector('h5').textContent.trim();
        const rows = category.querySelectorAll('tr');
        const headers = ["Nom de l'article", "Quantité", "Commentaire"];
        const data = Array.from(rows).map(row => {
        const cells = row.querySelectorAll('td');
        const commentaire = cells[2]?.querySelector('i')?.getAttribute('data-bs-content') || '';
        return [
            cells[0]?.textContent.trim() || '', // Item Name
            cells[1]?.textContent.trim() || '', // Quantity
            commentaire // Commentaire
        ];
    });

        // Estimate table height
        const estimatedTableHeight = (data.length + 1) * 10; // Approx 10mm per row including header

        // Check if the table fits on the current page
        if (cursorY + 20 + estimatedTableHeight > pageHeight) {
            pdf.addPage();
            cursorY = 10;
        }

        // Add category name
        pdf.setFontSize(14);
        pdf.text(categoryName, pageWidth / 2, cursorY, { align: "center" });
        cursorY += 10;

        // Add table
        pdf.autoTable({
            head: [headers],
            body: data,
            startY: cursorY,
            theme: 'grid',
            styles: {
                font: 'Arial',
                halign: 'center',
                valign: 'middle',
            },
            headStyles: {
                fillColor: [200, 200, 200],
                textColor: 0,
                fontStyle: 'bold',
            },
            margin: { left: 30, right: 30 },
        });

        cursorY = pdf.lastAutoTable.finalY + 10; // Update cursorY
    });

    pdf.save('Verification-Checklist.pdf');
}

document.addEventListener('DOMContentLoaded', function () {
        const categoryHeaders = document.querySelectorAll('.category-header');

        categoryHeaders.forEach(header => {
            header.addEventListener('click', function () {
                const target = document.querySelector(this.getAttribute('data-bs-target'));

                if (target.classList.contains('show')) {
                    target.classList.remove('show');
                } else {
                    // Collapse other open sections
                    document.querySelectorAll('.collapse.show').forEach(openSection => {
                        openSection.classList.remove('show');
                    });

                    // Expand the clicked section
                    target.classList.add('show');
                }
            });
        });
    });




// Helper function to format quantity
function formatQuantity(quantity) {
    // Convert the quantity to a float
    const numQuantity = parseFloat(quantity);
    
    // Return formatted quantity
    // If the quantity is an integer, return without decimals
    // Otherwise return with decimal places intact
    return Number.isInteger(numQuantity) ? numQuantity.toFixed(0) : numQuantity.toString();
}


// Store caches for products
const productDataCaches = {};

// Function to handle search input
function setupSearch(productSearchId, url, containerClass) {
    document.getElementById(productSearchId).addEventListener('input', function() {
        const query = this.value;
        fetch(`${url}?query=${query}`)
            .then(response => response.json())
            .then(data => renderProducts(data.products, containerClass))
            .catch(error => console.error('Error fetching products:', error));
    });
}

// Function to render products in modal
function renderProducts(products, containerClass) {
    const productListContainer = document.querySelector(`.modal-body .row.${containerClass}`);
    productListContainer.innerHTML = ''; // Clear existing entries

    products.forEach(product => {
        const cachedData = productDataCaches[product.id] || { quantity: product.checklist_quantity || 0, comment: product.commentaire || '' };
        
        const productHTML = `
            <div class="col-12 d-flex align-items-center justify-content-between product-item">
                <div class="product-info d-flex align-items-center">
                    <h6 class="product-name mb-0 me-3">${product.name}
                        <strong style="color: ${product.quantity <= 0 ? 'red' : 'green'};">(${formatQuantity(product.quantity)})</strong>
                    </h6>
                </div>
                <input type="hidden" name="product_ids[]" value="${product.id}">
                <div class="form-group d-flex align-items-center me-2">
                    <label for="quantity-${product.id}" class="form-label me-2">Quantité:</label>
                    <input type="number" class="form-control text-center quantity-input"
                           id="quantity-${product.id}" name="quantities[]"
                           min="0" value="${cachedData.quantity}" required
                           data-product-id="${product.id}">
                </div>
                <div class="form-group">
                    <button type="button" class="btn btn-secondary btn-sm toggle-comment" data-product-id="${product.id}">
                        <i class="fa fa-comment-dots"></i>
                    </button>
                    <textarea id="comment-${product.id}" class="form-control mt-2 comment-textarea"
                              name="commentaires[]" placeholder="NT pour nouvelle tablée"
                              style="display: none;" data-product-id="${product.id}">${cachedData.comment}</textarea>
                </div>
            </div>
        `;
        productListContainer.insertAdjacentHTML('beforeend', productHTML);
    });

    // Bind events for new elements
    bindCommentToggleEvents();
    bindQuantityInputEvents();
}

// Function to bind comment toggle events
function bindCommentToggleEvents() {
    document.querySelectorAll('.toggle-comment').forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.getAttribute("data-product-id");
            const target = document.querySelector(`textarea[data-product-id='${productId}']`);
            if (target) {
                target.style.display = (target.style.display === "none" || target.style.display === "") ? "block" : "none";
            }
        });
    });
}

// Function to track quantity input changes
function bindQuantityInputEvents() {
    document.querySelectorAll('.quantity-input').forEach(input => {
        input.addEventListener('input', function () {
            const productId = this.dataset.productId;
            if (!productDataCaches[productId]) {
                productDataCaches[productId] = {};
            }
            productDataCaches[productId].quantity = this.value;
        });
    });
}

// Initialize searches for each modal (customize for your needs)
document.addEventListener('DOMContentLoaded', function() {
    setupSearch('productSearch', searchProductsBaseUrl, 'rgh');
    setupSearch('productSearch1', searchProductsJetableUrl, 'rt');
    setupSearch('productSearch2', searchProductsDecorUrl, 'rtt');
    setupSearch('productSearch3', searchProductsBarUrl, 'rttt');
    setupSearch('productSearch4', searchProductsCafeUrl, 'rtttt');
    setupSearch('productSearch5', searchProductsDiversUrl, 'rttttt');
    setupSearch('productSearch6', searchProductsTableUrl, 'rtttttt');
    setupSearch('productSearch7', searchProductsVerreUrl, 'rttttttt');
    setupSearch('productSearch8', searchProductsPorcelaineUrl, 'rtttttttt');
    setupSearch('productSearch9', searchProductsCanapeUrl, 'rttttttttt');
    setupSearch('productSearch10', searchProductsCuissonUrl, 'rtttttttttt');
    setupSearch('productSearch11', searchProductsServiceUrl, 'rttttttttttt');
    setupSearch('productSearch12', searchProductsAlcoolFortUrl, 'rtttttttttttt');
    setupSearch('productSearch13', searchProductsBieresUrl, 'rttttttttttttt');
    setupSearch('productSearch14', searchProductsVinsUrl, 'rtttttttttttttt');
    setupSearch('productSearch15', searchProductsSansAlcoolUrl, 'rttttttttttttttt');
    setupSearch('productSearch16', searchProductsCFCDNUrl, 'rtttttttttttttttt');
    
    // Optionally, you may also want to handle search for any other additional modals dynamically.
});





// Handle quantity change and set status to 'en_cours'
document.addEventListener("DOMContentLoaded", function () {
    const quantityFields = document.querySelectorAll('input[name="quantity"]');

    quantityFields.forEach(function(field) {
        field.addEventListener("change", function() {
            const productId = this.id.split('-')[1];
            const statusField = document.getElementById("status-" + productId);

            // Set status to 'en_cours' on quantity change
            if (statusField) {
                statusField.value = "en_cours";
            }
        });
    });
});

// Submit Checklist Form Function
function submitChecklistForm(productId) {
    const form = document.getElementById(`checklistForm-${productId}`);
    const url = form.action;

    fetch(url, {
        method: 'POST',
        body: new FormData(form),
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCSRFToken()  // Ensure CSRF token is included
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            location.reload();  // Or update the quantity display dynamically
        } else {
            alert(data.message);
        }
    })
    .catch(error => console.error('Error:', error));
}

// Retrieve CSRF token function
function getCSRFToken() {
    return document.querySelector("[name=csrfmiddlewaretoken]").value;
}

// Toggle Section Visibility
function toggleSection(sectionId) {
    const section = document.getElementById(sectionId);
    section.classList.toggle("hidden");
}

// Modal Functions
function openModal(imageUrl) {
    const modal = document.getElementById("photoModal");
    const modalImg = document.getElementById("modalImg");
    const downloadBtn = document.getElementById("downloadBtn");

    // Set image URL for display and download
    modalImg.src = imageUrl;
    downloadBtn.href = imageUrl;

    modal.style.display = "flex";  // Show modal with flex centering
}

function closeModal() {
    document.getElementById("photoModal").style.display = "none";
}

function calculateDifference(productId) {
    const initialQuantity = parseInt(document.getElementById(`initial-quantity-${productId}`).value);
    const currentQuantity = parseInt(document.getElementById(`quantity-${productId}`).value);

    const difference = currentQuantity - initialQuantity;

    // Display the difference
    const differenceElement = document.getElementById(`quantity-difference-${productId}`);
    if (difference !== 0) {
        differenceElement.innerHTML = `Différence: ${difference > 0 ? '+' : ''}${difference}`;
        differenceElement.style.color = difference > 0 ? 'green' : 'red';
    } else {
        differenceElement.innerHTML = '';
    }
}







document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('searchItems');
    const itemList = document.getElementById('itemList');
    const categories = itemList.querySelectorAll('.category-group');

    function filterItems() {
        const searchQuery = searchInput.value.toLowerCase();

        categories.forEach(category => {
            const items = category.querySelectorAll('.item');
            let categoryVisible = false;

            items.forEach(item => {
                const itemName = item.getAttribute('data-name').toLowerCase();
                if (itemName.includes(searchQuery)) {
                    item.style.display = '';
                    categoryVisible = true;
                } else {
                    item.style.display = 'none';
                }
            });

            // Show/hide category based on item visibility
            category.style.display = categoryVisible ? '' : 'none';
        });
    }

    searchInput.addEventListener('input', filterItems);
});

document.addEventListener('DOMContentLoaded', function () {
    // Initialize all popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    const popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
});


$(document).ready(function() {
    // Handle document form submission
    $('#documentForm').submit(function(event) {
        event.preventDefault(); // Prevent default form submission

        var formData = new FormData(this); // Collect form data

        $.ajax({
            url: uploadDocumentUrl, // Adjust your URL here
            method: "POST",
            data: formData,
            processData: false,
            contentType: false,
            success: function(data) {
                alert("Document téléchargé avec succès !");
                // You might append the new document to the list here
                location.reload(); // Optionally reload if you update the list dynamically
            },
            error: function(xhr, status, error) {
                alert("Error");
            }
        });
    });

    function getCSRFToken() {
        const name = "csrftoken=";
        const decodedCookie = decodeURIComponent(document.cookie);
        const cookieArray = decodedCookie.split(';');
        for (let i = 0; i < cookieArray.length; i++) {
            let cookie = cookieArray[i];
            while (cookie.charAt(0) === ' ') {
                cookie = cookie.substring(1);
            }
            if (cookie.indexOf(name) === 0) {
                return cookie.substring(name.length, cookie.length);
            }
        }
        return ""; // CSRF token not found
    }
    

    $('.delete-doc').click(function() {
    var docId = $(this).data('id');
    if (confirm("Es-tu sûr de vouloir supprimer ce document ?")) {
        $.ajax({
            url: "/delete_document/" + docId + "/", // This path should match your urls.py
            method: "POST",
            headers: {
                "X-CSRFToken": getCSRFToken()
            },
            success: function(data) {
                alert("Document supprimé !");
                location.reload(); // Reload page or update the list dynamically
            },
            error: function(xhr, status, error) {
                alert("Error");
            }
        });
    }
});


    // Handle document edit, implement as needed...
});

