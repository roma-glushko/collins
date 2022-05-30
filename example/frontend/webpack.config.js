module.exports = {
    entry: {
        "document-list": "./js/DocumentList.tsx",
        "document-view": "./js/DocumentView.tsx",
    },
    target: "web",
    module: {
        rules: [
            {
                test: /\.(ts|tsx)$/,
                loader: "awesome-typescript-loader",
            },
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
        extensions: [".js", ".jsx", ".json", ".ts", ".tsx"],
    },
    output: {
        path: __dirname + "/dist",
        filename: "[name].bundle.js",
    },
};