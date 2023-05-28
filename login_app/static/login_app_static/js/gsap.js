
const timeline = gsap.timeline({ defaults: { duration: 1 }})
timeline
    .from('.header', { x: '-50%', ease: 'power3' })
    .from('.gsap-content', { y: '300%', ease: 'power3' }, '<.4');

// const time2 = gsap.timeline({ defaults: { duration: 1 }})
