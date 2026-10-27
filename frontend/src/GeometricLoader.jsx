
import "./GeometricLoader.css";

const COUNT = 1500;
const GOLDEN_ANGLE = Math.PI * (3 - Math.sqrt(5));

const particles = Array.from({ length: COUNT }, (_, i) => {
  // Fibonacci sphere distribution for even particle coverage
  const y = 1 - (i / (COUNT - 1)) * 2;
  const radius = Math.sqrt(1 - y * y);
  const angle = GOLDEN_ANGLE * i;

  const x = 50 + Math.cos(angle) * radius * 43;
  const py = 50 + y * 43;

  // Smaller pixels create a dense digital texture
  const bright = i % 31 === 0 || i % 47 === 0;
  const size = bright ? 0.75 + (i % 3) * 0.2 : 0.22 + (i % 4) * 0.1;

  return {
    x,
    y: py,
    size,
    bright,
    depth: Math.sin(angle * 0.73 + i * 0.17),
    delay: `${-((i * 13) % 40) / 10}s`,
  };
});

// Connect nearby particles for a fine network effect
const connections = [];

for (let i = 0; i < COUNT; i += 2) {
  const a = particles[i];
  const b = particles[(i + 17) % COUNT];
  const distance = Math.hypot(a.x - b.x, a.y - b.y);

  if (distance > 1.2 && distance < 8) {
    connections.push({
      id: i,
      x1: a.x,
      y1: a.y,
      x2: b.x,
      y2: b.y,
    });
  }
}

export default function GeometricLoader() {
  return (
    <div
      className="geo-loader"
      role="img"
      aria-label="Animated golden pixel network sphere"
    >
      <div className="geo-loader-glow" />

      <svg
        className="geo-loader-shape"
        viewBox="0 0 100 100"
        aria-hidden="true"
      >
        <defs>
          <clipPath id="geoSphereClip">
            <circle cx="50" cy="50" r="44" />
          </clipPath>
          <filter id="geoNodeGlow" x="-200%" y="-200%" width="500%" height="500%">
            <feGaussianBlur stdDeviation="0.55" />
          </filter>
        </defs>

        {/* No filled circle: the pixels define the sphere's silhouette */}
        <g clipPath="url(#geoSphereClip)">
          <g className="geo-connections">
            {connections.map((line) => (
              <line
                key={line.id}
                x1={line.x1}
                y1={line.y1}
                x2={line.x2}
                y2={line.y2}
                stroke="#D5A85A"
                strokeWidth="0.12"
                opacity="0.32"
              />
            ))}
          </g>

          <g className="geo-pixels">
            {particles.map((p, i) => (
              <rect
                key={i}
                className={`geo-pixel ${p.bright ? "is-bright" : ""}`}
                x={p.x - p.size / 2}
                y={p.y - p.size / 2}
                width={p.size}
                height={p.size}
                fill={p.bright ? "#FFF0B5" : "#D5A85A"}
                opacity={
                  p.bright
                    ? 0.98
                    : 0.25 + ((p.depth + 1) / 2) * 0.5
                }
                style={{ "--pixel-delay": p.delay }}
              />
            ))}
          </g>

          {/* Soft glow only around the brightest square nodes */}
          <g filter="url(#geoNodeGlow)">
            {particles.filter((p) => p.bright).map((p, i) => (
              <rect
                key={i}
                x={p.x - p.size}
                y={p.y - p.size}
                width={p.size * 2}
                height={p.size * 2}
                fill="#F4D98B"
                opacity="0.5"
              />
            ))}
          </g>
        </g>
      </svg>
    </div>
  );
}

<g className="geo-pixels">
  {particles.map((p, i) => (
    <rect
      key={i}
      className={`geo-pixel ${p.bright ? "is-bright" : ""}`}
      x={p.x - p.size / 2}
      y={p.y - p.size / 2}
      width={p.size}
      height={p.size}
      fill={p.bright ? "#FFF0B5" : "#D5A85A"}
      opacity={
        p.bright
          ? 0.98
          : 0.25 + ((p.depth + 1) / 2) * 0.5
      }
      style={{
        "--pixel-delay": p.delay,
        "--pixel-duration": `${7 + (i % 11)}s`,
        "--drift-x": `${Math.sin(i * 12.9898) * 5}px`,
        "--drift-y": `${Math.cos(i * 7.233) * 5}px`,
      }}
    />
  ))}
</g>
