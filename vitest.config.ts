import path from "node:path";
import { pathToFileURL } from "node:url";

export default async function () {
  const serverRoot = path.resolve(
    process.env.SILVERBULLET_PATH || "../silverbullet",
  );
  const { default: serverConfig } = await import(
    pathToFileURL(path.join(serverRoot, "vitest.config.ts")).href
  );
  return {
    resolve: {
      alias: [
        ...serverConfig.resolve.alias,
        {
          find: "@silverbullet-server",
          replacement: path.join(serverRoot, "client"),
        },
      ],
    },
    test: { include: ["tests/**/*.test.ts"] },
  };
}
