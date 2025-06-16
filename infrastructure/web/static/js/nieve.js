// Crear el contenedor de nieve
const snowContainer = document.getElementById('snow-container');
const numberOfFlakes = 100; // Número de copos de nieve

// Crear copos de nieve y agregarlos al contenedor
for (let i = 0; i < numberOfFlakes; i++) {
    const flake = document.createElement('div');
    flake.classList.add('snowflake');
    flake.style.position = 'absolute';
    flake.style.width = '10px';
    flake.style.height = '10px';
    flake.style.backgroundColor = 'white';
    flake.style.borderRadius = '50%';
    flake.style.zIndex = '10001'; // Asegura que los copos se muestren por encima de otros elementos
    
    // Posición aleatoria inicial
    flake.style.left = `${Math.random() * window.innerWidth}px`;
    flake.style.top = `-10px`;

    // Agregar el copo de nieve al contenedor
    snowContainer.appendChild(flake);
    
    // Usar un retraso para hacer que los copos de nieve aparezcan de a poco
    setTimeout(() => {
        // Animar el copo de nieve
        flake.animate(
            [
                { transform: `translateY(0)` },
                { transform: `translateY(${window.innerHeight}px)` }
            ],
            {
                duration: Math.random() * 3000 + 3000, // Duración aleatoria entre 3s y 6s
                easing: 'linear',
                iterations: Infinity
            }
        );
    }, i * 100); // Retraso de 100 ms entre cada copo de nieve
}
