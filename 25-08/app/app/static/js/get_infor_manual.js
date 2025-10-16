const get_pdf_manual = document.getElementById("get_pdf_manual");
get_pdf_manual.addEventListener("click", () => {
    window.open("/api_inf_software/download_manual", "_blank"); 
});
