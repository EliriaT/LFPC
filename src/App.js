import Graph from "react-graph-vis";
import React, { useState } from "react";
import {
  Input,
  InputGroup,
  InputLeftAddon,
  Alert,
  AlertIcon,
  Button,
  AlertDescription,
  Center,
  Stack,
  Box,
} from "@chakra-ui/react";
const options = {
  layout: {
    hierarchical: false,
  },
  edges: {
    color: "#000000",
    smooth: {
      enabled: true,
      type: "discrete",
      roundness: 0.5,
    },
  },
  interaction: {
    hover: true,
    hoverConnectedEdges: true,
    selectable: true,
    selectConnectedEdges: true,
  },
};

function randomColor() {
  const red = Math.floor(Math.random() * 56 + 200)
    .toString(16)
    .padStart(2, "0");
  const green = Math.floor(Math.random() * 56 + 200)
    .toString(16)
    .padStart(2, "0");
  const blue = Math.floor(Math.random() * 56 + 200)
    .toString(16)
    .padStart(2, "0");
  return `#${red}${green}${blue}`;
}

const App = () => {
  const [notTerm, setNotTerm] = useState("");
  const [term, setTerm] = useState("");
  const [prod, setProd] = useState("");
  const [word, setWord] = useState({
    text: "",
    isSubmitted: false,
    status: "error",
    errorDescript: "Meaw",
  });
  const [adic, setAdic] = useState();
  var aadd;

  let angle = Math.PI;
  const createEdge = (a, b, c) => {
    const color = randomColor();
    setState(({ graph: { nodes, edges }, counter, ...rest }) => {
      const id = counter;
      const from = Math.floor(Math.random() * (counter - 1)) + 1;
      return {
        graph: {
          nodes: nodes,
          edges: [
            ...edges,
            {
              from: a,
              to: b,
              label: c,
              selfReference: { angle: (angle += 1) },
            },
          ],
        },
        counter: id,
        ...rest,
      };
    });
  };

  const createNode = (c) => {
    const color = randomColor();
    setState(({ graph: { nodes, edges }, counter, ...rest }) => {
      const id = counter + 1;
      return {
        graph: {
          nodes: [
            ...nodes,
            { id, label: `q${id}(${c != undefined ? c : ""})`, color },
          ],
          edges: edges,
        },
        counter: id,
        ...rest,
      };
    });
  };

  const [state, setState] = useState({
    counter: -1,
    graph: {
      nodes: [],
      edges: [],
    },
    events: {
      select: ({ nodes, edges }) => {
        console.log("Selected nodes:");
        console.log(nodes);
        console.log("Selected edges:");
      },
    },
  });

  const { graph, events } = state;

  const dfs = (node, cur, term, pos) => {
    console.log(cur);
    if (cur.length === word.text.length && term) {
      if (cur.localeCompare(word.text) === 0) {
        word.status = "success";
      }
      return;
    }

    if (cur.length > word.text.length) return;

    for (let i = 0; i < aadd[0].length; i++) {
      if (aadd[node][i].exists === true) {
        for (let j = 0; j < aadd[node][i].name.length; j++) {
          if (word.text[pos] === aadd[node][i].name[j]) {
            dfs(
              i,
              cur + aadd[node][i].name[j],
              aadd[node][i].terminal[j],
              pos + 1
            );
          }
        }
      }
    }

    return;
  };

  const createGraph = (notTerm, term, prod, word) => {
    setState({
      counter: -1,
      graph: {
        nodes: [],
        edges: [],
      },
      events: {
        select: ({ nodes, edges }) => {
          console.log("Selected nodes:");
          console.log(nodes);
          console.log("Selected edges:");
        },
      },
    });

    const a = notTerm.replaceAll(" ", "").split(",");
    const b = term.replaceAll(" ", "").split(",");
    const c = prod.replaceAll(" ", "").split(",");

    const used = [];

    aadd = new Array(a.length + 1).fill().map(() =>
      new Array(a.length + 1).fill().map(
        () =>
          new Object({
            exists: false,
            name: [],
            terminal: [],
          })
      )
    );

    console.log(aadd);

    //C->gP
    //P->nM

    c.forEach((e) => {
      const temp1 = used.findIndex((x) => x === e[0]);
      const temp2 = used.findIndex((x) => x === e[4]);
      if (temp1 == -1) {
        createNode(e[0]);
        used.push(e[0]);
      }
      if (temp2 == -1 && e[0] != e[4]) {
        createNode(e[4]);
        used.push(e[4]);
      }

      const from = used.findIndex((x) => x === e[0]);
      const to = used.findIndex((x) => x === e[4]);
      aadd[from][to] = {
        ...aadd[from][to],
        exists: true,
      };

      if (e.length < 5) {
        aadd[from][to].terminal.push(true);
      } else {
        aadd[from][to].terminal.push(false);
      }
      aadd[from][to].name.push(e[3]);
      createEdge(from, to, e[3]);

    });
    console.log(aadd);
    if (word != "") dfs(0, "", false, 0);
  };

  return (
    <>
      <Box bg="#BEE3F8" w="100%" p={2} color="white" boxShadow="dark-lg">
        <Center p={4} fontSize="xl" color="#1A365D">
          Laborator 1
        </Center>
        <Stack spacing={2}>
          <InputGroup>
            <InputLeftAddon children="Vn" bg="teal" />
            <Input
              onChange={(e) => setNotTerm(e.target.value)}
              type="text"
              placeholder="S, A, B, C"
              bg="#F0FFF4"
              color="#1A365D"
            />
          </InputGroup>

          <InputGroup>
            <InputLeftAddon children="Vt" bg="teal" />
            <Input
              onChange={(e) => setTerm(e.target.value)}
              type="text"
              placeholder="a, b"
              bg="#F0FFF4"
              color="#1A365D"
            />
          </InputGroup>

          <InputGroup>
            <InputLeftAddon children="Pr" bg="teal" />
            <Input
              onChange={(e) => setProd(e.target.value)}
              type="text"
              placeholder="S->aA, A->bS, A->aB, B->bC, C->aA, C->b"
              bg="#F0FFF4"
              color="#1A365D"
            />
          </InputGroup>

          <InputGroup>
            <InputLeftAddon children="W" bg="teal" />
            <Input
              id="W"
              onChange={(e) =>
                setWord({
                  ...word,
                  text: e.target.value,
                  isSubmitted: false,
                  status: "error",
                })
              }
              type="text"
              placeholder="aaaabc"
              bg="#F0FFF4"
              color="#1A365D"
            />
          </InputGroup>

          <Center>
            <Button
              onClick={() => {
                const valide = createGraph(notTerm, term, prod, word.text);
                setWord({ ...word, isSubmitted: true });
              }}
              colorScheme="teal"
              type="submit"
              mt={4}
              size="sm"
            >
              Submit
            </Button>
          </Center>
        </Stack>
      </Box>
      {word.isSubmitted && word.text != "" && (
        <Alert status={word.status}>
          <AlertIcon />
          <AlertDescription>{word.errorDescript}</AlertDescription>
        </Alert>
      )}

      <Graph
        graph={graph}
        options={options}
        events={events}
        style={{ height: "640px" }}
      />
    </>
  );
};

export default App;
