const mapCanvas = document.getElementById('mapCanvas');
const yearDisplay = document.getElementById('yearDisplay');
const slider = document.getElementById('slider');

const imageDirectory = 'png_maps/';

function updateYear(year) {
    yearDisplay.textContent = `Year: ${year}`;
    
   
    const img = document.createElement('img');
    img.src = `${imageDirectory}PRISM_ppt_stable_4kmM3_${year}_bil.png`;
    img.style.maxWidth = '100%';
    img.style.height = 'auto';  // Automatically maintain aspect ratio
    
    mapCanvas.innerHTML = '';
    mapCanvas.appendChild(img);
}

updateYear(slider.value);
