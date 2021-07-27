import React from "react";

const Rating = ({ value, text, color }) => {
  let stars = [];
  let val = parseInt(value);
  let rem = parseFloat(value) - val;
  for (let i = 0; i < val; i++) {
    stars.push(
      <span>
        <i style={{ color: color }} className="fas fa-star"></i>
      </span>
    );
  }
  if (rem >= 0.5) {
    stars.push(
      <span>
        <i style={{ color }} className="fas fa-star-half-alt"></i>
      </span>
    );
  }
  for (let i = val + (rem >= 0.5 ? 1 : 0); i < 5; i++) {
    stars.push(
      <span>
        <i style={{ color }} className="far fa-star"></i>
      </span>
    );
  }

  return (
    <div className="rating">
      {stars.map((star) => star)}
      <span>{text && text}</span>
    </div>
  );
};

export default Rating;
