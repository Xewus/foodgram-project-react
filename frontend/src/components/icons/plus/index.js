import * as React from "react";

const PlusIcon = (props) => {
  return (
    <svg
      width={16}
      height={17}
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      {...props}
    >
      <path
        d="M8 1.5v14M1 8.5h14"
        stroke={props.fill || '#fff'}
        strokeWidth={2}
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

export default PlusIcon