// JavaScript code to close the tooltip on clicking outside

document.addEventListener("DOMContentLoaded", function () {
    document.addEventListener("click", function (event) {
      // Close tooltip if clicked outside the tooltip
      if (!event.target.closest(".tooltip")) {
        document.querySelectorAll(".tooltip-box").forEach(function (tooltipBox)
        {
          tooltipBox.style.display = "none";
        });
      }
    });
});