import * as React from "react";

function SvgBigIcon(props) {
  return (
    <svg
      width={32}
      height={31}
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      {...props}
    >
      <path
        d="M16 1l4.635 9.39L31 11.905l-7.5 7.305 1.77 10.32L16 24.655 6.73 29.53 8.5 19.21 1 11.905l10.365-1.515L16 1z"
        stroke="#F9A62B"
        fill="#F9A62B"
        strokeWidth={2}
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

export default SvgBigIcon