{
  "includes": [ "deps/common-sqlite.gypi" ],
  "variables": {
      "sqlite%":"internal",
      "sqlite_libname%":"sqlite3",
      "module_name": "node_sqlite3",
      "napi_version": "6",
      "platform": "<!(node -p \"process.platform\")",
      "module_path": "./lib/binding/napi-v<(napi_version)-<(platform)-<(target_arch)",
      "debug": 0,
      "debug_output_path": "./debug",
  },
  
  "targets": [
    {
      "target_name": "<(module_name)",
      "cflags!": [ "-fno-exceptions" ],
      "cflags_cc!": [ "-fno-exceptions" ],
      "defines!": [
				"-std=c++11"
			],
      "xcode_settings": { 
        "GCC_ENABLE_CPP_EXCEPTIONS": "YES",
        "CLANG_CXX_LIBRARY": "libc++",
        "MACOSX_DEPLOYMENT_TARGET": "10.14",
        "EXCUTABLE_EXTENSION": "node",
        "OTHER_CFLAGS": [
          "-ObjC++",
          "-g"
        ],
        "DEBUG_INFORMATION_FORMAT": "dwarf-with-dsym",
        "GCC_GENERATE_DEBUGGING_SYMBOLS": "YES",
        "GCC_OPTIMIZATION_LEVEL": "0",
        "OTHER_CFLAGS": ["-O0"],
        "conditions": [
          ["debug==1", {
            
          }],
          ["debug!=1", {
            "GCC_OPTIMIZATION_LEVEL": "3",
            "OTHER_CFLAGS": ["-O3"]
          }]
        ]
      },
      "msvs_settings": {
        "VCCLCompilerTool": { 
          "ExceptionHandling": 1,
          "Optimization": 0,
          "DebugInformationFormat": 3,
        },
        "VCLinkerTool": {
          "GenerateDebugInformation": "true",  # 始终生成调试信息
          "ProgramDatabaseFile": "$(OutDir)$(TargetName).pdb"
        }
      },
      "include_dirs": [
        "<!@(node -p \"require(\'node-addon-api\').include\")"],
      "conditions": [
        ["sqlite != \"internal\"", {
            "include_dirs": [
              "<!@(node -p \"require('node-addon-api').include\")", "<(sqlite)/include" ],
            "libraries": [
               "-l<(sqlite_libname)"
            ],
            "conditions": [ [ "OS==\"linux\"", {"libraries+":["-Wl,-rpath=<@(sqlite)/lib"]} ] ],
            "conditions": [ [ "OS!=\"win\"", {"libraries+":["-L<@(sqlite)/lib"]} ] ],
            "msvs_settings": {
              "VCLinkerTool": {
                "AdditionalLibraryDirectories": [
                  "<(sqlite)/lib"
                ]
              }
            }
        },
        {
            "dependencies": [
              "<!(node -p \"require('node-addon-api').gyp\")",
              "deps/sqlite3.gyp:sqlite3"
            ]
        }
        ]
      ],
      "sources": [
        "src/backup.cc",
        "src/database.cc",
        "src/node_sqlite3.cc",
        "src/statement.cc"
      ],
      "defines": [ 
        "NAPI_VERSION=<(napi_version)",
        "NAPI_DISABLE_CPP_EXCEPTIONS=1",
        "DEBUG=<(debug)"
      ]
    },
    {
      "target_name": "action_after_build",
      "type": "none",
      "dependencies": [ "<(module_name)" ],
      "copies": [
          {
            "files": [ "<(PRODUCT_DIR)/<(module_name).node" ],
            "destination": "<(module_path)"
          }
      ]
    }
  ]
}
