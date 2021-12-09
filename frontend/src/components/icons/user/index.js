const UserIcon = (props) => {
  return (
    <svg
      width={20}
      height={20}
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      {...props}
    >
      <path
        d="M17.5 18.333V16.39c0-1.031-.417-2.02-1.16-2.75a3.994 3.994 0 00-2.798-1.139H5.625c-1.05 0-2.057.41-2.799 1.139a3.855 3.855 0 00-1.16 2.75v1.944M9.583 9.167a3.75 3.75 0 100-7.5 3.75 3.75 0 000 7.5z"
        stroke="#000"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

export default UserIcon