import React, { useState } from "react";
import { Button, Form, FormControl } from "react-bootstrap";
import { useHistory } from "react-router-dom";

const SearchBox = () => {
  const [keyword, setKeyword] = useState("");

  let history = useHistory();

  const submitHandler = (e) => {
    e.preventDefault();
    if (keyword) {
      //when we start search, we want to start from page1
      history.push(`/?keyword=${keyword}&page=1`);
    } else {
      history.push(history.push(history.location.pathname));
    }
  };
  return (
    <Form onSubmit={submitHandler} className="d-flex">
      <FormControl
        placeholder="Search"
        aria-label="Search"
        type="text"
        name="q"
        onChange={(e) => setKeyword(e.target.value)}
        className="mr-sm-2 ml-sm-5"
      />
      <Button type="submit" variant="outline-success">
        Search
      </Button>
    </Form>
  );
};

export default SearchBox;
