import { FastApiLink } from "./constants";
import { componentTypes } from "./types";

export interface PCConfiguration {
  cpu: number;
  case: number;
  psu: number;
  [key: string]: number;
}

export async function fetchCompatible(
  configuration: PCConfiguration,
  comp: string
) {

  const validComponent = componentTypes.find((c) => c.id === comp);

  if (!validComponent) {
    throw new Error(`Invalid component type: ${comp}`);
  }
  
  const endpoint = `${FastApiLink}/${comp}`;
  
  const response = await fetch(endpoint, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(configuration),
  });
  
  if (!response.ok) {
    throw new Error(`Failed to fetch compatible ${comp.toUpperCase()}`);
  }
  
  return response.json();
}
