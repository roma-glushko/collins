module.exports = {
    entry: {
        main: "./js/LiveArea.jsx",
    },
    module: {
        rules: [
            {
                test: /\.jsx$/,
                // exclude: /node_modules/,
                use: "babel-loader",
            },
            {
                test: /\.(svg|png|jpg|jpeg|gif)$/,
                loader: "file-loader",

                options: {
                    name: "[name].[ext]",
                    outputPath: "./dist",
                },
            },
            {
                test: /\.css$/i,
                use: ["style-loader", "css-loader"],
            },
        ],
    },
    resolve: {
        extensions: [".js", ".jsx"],
    },
    output: {
        path: __dirname + "/dist",
        filename: "[name].bundle.js",
    },
};