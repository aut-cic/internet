const path = require("node:path");
const CssMinimizerPlugin = require("css-minimizer-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

// Production mode already minifies the JS via webpack's built-in TerserPlugin;
// CssMinimizerPlugin below is what minifies the extracted stylesheet.

module.exports = {
  mode: "production",
  entry: "./src/index.ts",
  output: {
    filename: "[name].bundle.js",
    path: path.resolve(__dirname, "dist"),
    // Emitted assets (fonts, icons) are fetched relative to this, and the app
    // serves frontend/dist at /static.
    publicPath: "/static/",
    clean: true,
  },

  resolve: {
    extensions: [".ts", ".js"],
  },

  optimization: {
    // "..." keeps the default JS minimizer; without it Terser is replaced.
    minimizer: [
      "...",
      new CssMinimizerPlugin({
        minimizerOptions: {
          preset: [
            "default",
            // Bootstrap embeds SVGs as data: URIs that svgo cannot parse, so it
            // errors out on them anyway. Turning it off drops the warning
            // without losing optimisation that was never happening.
            { svgo: false },
          ],
        },
      }),
    ],
  },

  // rtlcss reports "unsupported directive" for Bootstrap's
  // --bs-breadcrumb-divider and its inline data: URIs. It leaves them alone,
  // which is the correct outcome -- neither should be direction-flipped. The
  // match is deliberately narrow so real rtlcss problems still surface.
  ignoreWarnings: [
    {
      module: /bootstrap\.scss/,
      message: /from "rtlcss" plugin: unsupported directive/,
    },
  ],

  plugins: [new MiniCssExtractPlugin({ filename: "[name].css" })],

  module: {
    rules: [
      { test: /\.ts$/, use: "ts-loader" },
      // Plain CSS (app.css, gauge.css, fonts.css, bootstrap-icons) is authored
      // RTL-natively -- `direction: rtl`, `right:`, `text-align: right`. It must
      // NOT go through rtlcss, which would flip it back to LTR.
      {
        test: /\.css$/,
        use: [MiniCssExtractPlugin.loader, "css-loader"],
      },
      // Only bootstrap.scss matches here. Bootstrap compiles LTR from source, so
      // rtlcss flips it, giving us one RTL copy of the framework with our
      // palette instead of bundling the prebuilt RTL build as a second copy.
      {
        test: /\.s[ac]ss$/i,
        use: [
          MiniCssExtractPlugin.loader,
          "css-loader",
          {
            loader: "postcss-loader",
            options: {
              postcssOptions: { plugins: [require("rtlcss")] },
            },
          },
          {
            loader: "sass-loader",
            options: {
              // Our own Sass is @use-clean. The remaining deprecation warnings
              // all come from bootstrap/scss/_functions.scss (@import plus the
              // global red()/green()/blue() functions) and cannot be fixed from
              // here. Silencing dependencies keeps the build quiet enough that
              // a deprecation in OUR code is actually visible.
              //
              // quietDeps only applies to files resolved through loadPaths --
              // a relative "../node_modules/..." URL counts as first-party and
              // stays noisy, which is why bootstrap is imported by package name.
              sassOptions: {
                quietDeps: true,
                loadPaths: [path.resolve(__dirname, "node_modules")],
              },
            },
          },
        ],
      },
    ],
  },
};
