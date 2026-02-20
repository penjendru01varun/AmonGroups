// AmonGroups Futuristic Website Logic
document.addEventListener('DOMContentLoaded', () => {
    initCosmicBackground();
    initMeteors();
    initGSAPAnimations();
    initTypingEffect();
    initTiltEffect();
    initCounterAnimation();
    initNavInteraction();
    initSparkleTrail();
});

// --- 1. Three.js Cosmic Background ---
function initCosmicBackground() {
    const canvas = document.querySelector('#cosmic-bg');
    if (!canvas) return;
    const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.z = 5;

    const particlesGeometry = new THREE.BufferGeometry();
    const particlesCount = 8000;
    const posArray = new Float32Array(particlesCount * 3);

    for (let i = 0; i < particlesCount * 3; i++) {
        posArray[i] = (Math.random() - 0.5) * 15;
    }

    particlesGeometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
    const particlesMaterial = new THREE.PointsMaterial({
        size: 0.005,
        color: '#00FFF5',
        transparent: true,
        opacity: 0.8,
        blending: THREE.AdditiveBlending
    });

    const particlesMesh = new THREE.Points(particlesGeometry, particlesMaterial);
    scene.add(particlesMesh);

    const shapesGroup = new THREE.Group();
    scene.add(shapesGroup);

    const geometries = [
        new THREE.OctahedronGeometry(1.5, 0),
        new THREE.TorusGeometry(1, 0.3, 16, 100),
        new THREE.IcosahedronGeometry(1, 0)
    ];

    const material = new THREE.MeshPhongMaterial({
        color: 0x6C63FF,
        wireframe: true,
        transparent: true,
        opacity: 0.2
    });

    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
    scene.add(ambientLight);

    const pointLight = new THREE.PointLight(0x00FFF5, 1);
    pointLight.position.set(5, 5, 5);
    scene.add(pointLight);

    for (let i = 0; i < 5; i++) {
        const mesh = new THREE.Mesh(geometries[Math.floor(Math.random() * geometries.length)], material);
        mesh.position.set((Math.random() - 0.5) * 10, (Math.random() - 0.5) * 10, (Math.random() - 0.5) * 5);
        mesh.rotation.set(Math.random() * Math.PI, Math.random() * Math.PI, 0);
        shapesGroup.add(mesh);
    }

    function animate() {
        requestAnimationFrame(animate);
        particlesMesh.rotation.y += 0.0005;
        particlesMesh.rotation.x += 0.0002;

        shapesGroup.children.forEach(mesh => {
            mesh.rotation.x += 0.01;
            mesh.rotation.y += 0.005;
            mesh.position.y += Math.sin(Date.now() * 0.001) * 0.002;
        });

        renderer.render(scene, camera);
    }

    animate();

    window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });
}

// --- 2. Falling Meteors ---
function initMeteors() {
    const starField = document.querySelector('#star-field');
    if (!starField) return;

    function createMeteor() {
        const meteor = document.createElement('div');
        meteor.className = 'meteor';
        const startX = Math.random() * window.innerWidth;
        const startY = Math.random() * -100;
        const duration = Math.random() * 2 + 1;

        meteor.style.cssText = `
            position: fixed; top: ${startY}px; left: ${startX}px;
            width: 2px; height: 50px; background: linear-gradient(to bottom, transparent, #00FFF5);
            opacity: ${Math.random()}; transform: rotate(45deg); z-index: -1; pointer-events: none;
        `;

        starField.appendChild(meteor);
        gsap.to(meteor, {
            top: window.innerHeight + 100,
            left: startX + 500,
            duration: duration,
            ease: "none",
            onComplete: () => { meteor.remove(); createMeteor(); }
        });
    }

    for (let i = 0; i < 8; i++) {
        setTimeout(createMeteor, Math.random() * 5000);
    }
}

// --- 3. Animations ---
function initGSAPAnimations() {
    gsap.registerPlugin(ScrollTrigger);
    document.querySelectorAll('[data-reveal]').forEach(el => {
        gsap.from(el, {
            scrollTrigger: { trigger: el, start: "top 85%" },
            y: 50, opacity: 0, duration: 1, ease: "power2.out"
        });
    });

    gsap.from('.hero-title', { opacity: 0, y: 30, duration: 1.2, delay: 0.5 });
    gsap.from('.hero-subtext', { opacity: 0, y: 20, duration: 1, delay: 0.8 });
    gsap.from('.hero-ctas', { opacity: 0, scale: 0.9, duration: 0.8, delay: 1.1 });
}

// --- 4. Typing ---
function initTypingEffect() {
    const textEl = document.querySelector('.typed-text');
    if (!textEl) return;
    const text = textEl.innerText;
    textEl.innerText = '';
    let i = 0;
    function type() {
        if (i < text.length) {
            textEl.innerText += text.charAt(i);
            i++;
            setTimeout(type, 50);
        }
    }
    setTimeout(type, 1500);
}

// --- 5. Tilt ---
function initTiltEffect() {
    document.querySelectorAll('.tilt').forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            const rotateX = (y - centerY) / 20;
            const rotateY = (centerX - x) / 20;
            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.05, 1.05, 1.05)`;
        });
        card.addEventListener('mouseleave', () => {
            card.style.transform = `perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)`;
        });
    });
}

// --- 6. Counters ---
function initCounterAnimation() {
    document.querySelectorAll('.count-up').forEach(counter => {
        const target = +counter.getAttribute('data-target');
        ScrollTrigger.create({
            trigger: counter, start: "top 90%",
            onEnter: () => {
                let count = 0;
                const increment = target / 100;
                const updateCount = () => {
                    if (count < target) { count += increment; counter.innerText = Math.ceil(count); setTimeout(updateCount, 10); }
                    else { counter.innerText = target; }
                }
                updateCount();
            }
        });
    });
}

// --- 7. Nav ---
function initNavInteraction() {
    const nav = document.querySelector('#navbar');
    const mobileBtn = document.querySelector('#mobile-menu-btn');
    const navLinks = document.querySelector('.nav-links');
    if (!nav) return;

    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) nav.classList.add('nav-scrolled');
        else nav.classList.remove('nav-scrolled');

        const sections = document.querySelectorAll('section');
        let current = "";
        sections.forEach(s => {
            if (pageYOffset >= s.offsetTop - 150) current = s.getAttribute('id');
        });
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href').includes(current)) link.classList.add('active');
        });
    });

    if (mobileBtn) mobileBtn.addEventListener('click', () => navLinks.classList.toggle('active'));
}

// --- 8. Sparkle Trail ---
function initSparkleTrail() {
    document.addEventListener('mousemove', (e) => {
        const sparkle = document.createElement('div');
        sparkle.className = 'sparkle-trail';
        sparkle.style.left = e.pageX + 'px';
        sparkle.style.top = e.pageY + 'px';
        document.body.appendChild(sparkle);
        gsap.to(sparkle, {
            opacity: 0, y: Math.random() * 80 - 40, x: Math.random() * 80 - 40,
            duration: 1, ease: "power2.out", onComplete: () => sparkle.remove()
        });
    });
}
