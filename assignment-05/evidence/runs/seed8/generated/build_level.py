import json

PLACEMENTS = json.loads(r"""[
  {
    "name": "Arena_Floor",
    "role": "floor",
    "location": {
      "x": 0.0,
      "y": 0.0,
      "z": -10.0
    },
    "rotation": {
      "pitch": 0.0,
      "yaw": 0.0,
      "roll": 0.0
    },
    "folder": "ArenaGen/Shell",
    "visual_only": false,
    "asset_path": "/Engine/BasicShapes/Cube",
    "size_cm": {
      "x": 2400.0,
      "y": 1600.0,
      "z": 20.0
    },
    "scale": {
      "x": 24.0,
      "y": 16.0,
      "z": 0.2
    }
  },
  {
    "name": "Arena_Ceiling",
    "role": "ceiling",
    "location": {
      "x": 0.0,
      "y": 0.0,
      "z": 530.0
    },
    "rotation": {
      "pitch": 0.0,
      "yaw": 0.0,
      "roll": 0.0
    },
    "folder": "ArenaGen/Shell",
    "visual_only": false,
    "asset_path": "/Engine/BasicShapes/Cube",
    "size_cm": {
      "x": 2400.0,
      "y": 1600.0,
      "z": 20.0
    },
    "scale": {
      "x": 24.0,
      "y": 16.0,
      "z": 0.2
    }
  },
  {
    "name": "Wall_DoorwayEnd",
    "role": "wall",
    "location": {
      "x": 1220.0,
      "y": 0.0,
      "z": 260.0
    },
    "rotation": {
      "pitch": 0.0,
      "yaw": 0.0,
      "roll": 0.0
    },
    "folder": "ArenaGen/Shell",
    "visual_only": false,
    "asset_path": "/Engine/BasicShapes/Cube",
    "size_cm": {
      "x": 40.0,
      "y": 1600.0,
      "z": 520.0
    },
    "scale": {
      "x": 0.4,
      "y": 16.0,
      "z": 5.2
    }
  },
  {
    "name": "Wall_TrussEnd",
    "role": "wall",
    "location": {
      "x": -1220.0,
      "y": 0.0,
      "z": 260.0
    },
    "rotation": {
      "pitch": 0.0,
      "yaw": 0.0,
      "roll": 0.0
    },
    "folder": "ArenaGen/Shell",
    "visual_only": false,
    "asset_path": "/Engine/BasicShapes/Cube",
    "size_cm": {
      "x": 40.0,
      "y": 1600.0,
      "z": 520.0
    },
    "scale": {
      "x": 0.4,
      "y": 16.0,
      "z": 5.2
    }
  },
  {
    "name": "Railing_North",
    "role": "railing",
    "location": {
      "x": 0.0,
      "y": 810.0,
      "z": 60.0
    },
    "rotation": {
      "pitch": 0.0,
      "yaw": 0.0,
      "roll": 0.0
    },
    "folder": "ArenaGen/Shell",
    "visual_only": false,
    "asset_path": "/Engine/BasicShapes/Cube",
    "size_cm": {
      "x": 2400.0,
      "y": 20.0,
      "z": 120.0
    },
    "scale": {
      "x": 24.0,
      "y": 0.2,
      "z": 1.2
    }
  },
  {
    "name": "Railing_South",
    "role": "railing",
    "location": {
      "x": 0.0,
      "y": -810.0,
      "z": 60.0
    },
    "rotation": {
      "pitch": 0.0,
      "yaw": 0.0,
      "roll": 0.0
    },
    "folder": "ArenaGen/Shell",
    "visual_only": false,
    "asset_path": "/Engine/BasicShapes/Cube",
    "size_cm": {
      "x": 2400.0,
      "y": 20.0,
      "z": 120.0
    },
    "scale": {
      "x": 24.0,
      "y": 0.2,
      "z": 1.2
    }
  },
  {
    "name": "Doorway_Frame",
    "role": "obstacle",
    "location": {
      "x": 1175.0,
      "y": -455.8,
      "z": 150.0
    },
    "rotation": {
      "pitch": 0.0,
      "yaw": 0.0,
      "roll": 0.0
    },
    "folder": "ArenaGen/Landmarks",
    "visual_only": false,
    "asset_path": "/Engine/BasicShapes/Cube",
    "size_cm": {
      "x": 50.0,
      "y": 300.0,
      "z": 300.0
    },
    "scale": {
      "x": 0.5,
      "y": 3.0,
      "z": 3.0
    }
  },
  {
    "name": "Truss_Panel",
    "role": "obstacle",
    "location": {
      "x": -1175.0,
      "y": -470.2,
      "z": 150.0
    },
    "rotation": {
      "pitch": 0.0,
      "yaw": 0.0,
      "roll": 0.0
    },
    "folder": "ArenaGen/Landmarks",
    "visual_only": false,
    "asset_path": "/Engine/BasicShapes/Cube",
    "size_cm": {
      "x": 50.0,
      "y": 300.0,
      "z": 300.0
    },
    "scale": {
      "x": 0.5,
      "y": 3.0,
      "z": 3.0
    }
  },
  {
    "name": "Mezzanine_Strut_A",
    "role": "obstacle",
    "location": {
      "x": 1175.0,
      "y": 499.7,
      "z": 150.0
    },
    "rotation": {
      "pitch": 0.0,
      "yaw": 0.0,
      "roll": 0.0
    },
    "folder": "ArenaGen/Landmarks",
    "visual_only": false,
    "asset_path": "/Engine/BasicShapes/Cube",
    "size_cm": {
      "x": 50.0,
      "y": 300.0,
      "z": 300.0
    },
    "scale": {
      "x": 0.5,
      "y": 3.0,
      "z": 3.0
    }
  },
  {
    "name": "Mezzanine_Strut_B",
    "role": "obstacle",
    "location": {
      "x": -1175.0,
      "y": 374.7,
      "z": 150.0
    },
    "rotation": {
      "pitch": 0.0,
      "yaw": 0.0,
      "roll": 0.0
    },
    "folder": "ArenaGen/Landmarks",
    "visual_only": false,
    "asset_path": "/Engine/BasicShapes/Cube",
    "size_cm": {
      "x": 50.0,
      "y": 300.0,
      "z": 300.0
    },
    "scale": {
      "x": 0.5,
      "y": 3.0,
      "z": 3.0
    }
  },
  {
    "name": "Spawn_Player",
    "role": "spawn",
    "location": {
      "x": -125.0,
      "y": 0.0,
      "z": 94.0
    },
    "rotation": {
      "pitch": 0.0,
      "yaw": 0.0,
      "roll": 0.0
    },
    "folder": "ArenaGen/Spawns",
    "visual_only": true,
    "class_path": "/Script/Engine.PlayerStart"
  },
  {
    "name": "Spawn_Opponent",
    "role": "spawn",
    "location": {
      "x": 125.0,
      "y": 0.0,
      "z": 90.0
    },
    "rotation": {
      "pitch": 0.0,
      "yaw": 180.0,
      "roll": 0.0
    },
    "folder": "ArenaGen/Spawns",
    "visual_only": true,
    "class_path": "/Script/Engine.TargetPoint"
  }
]""")

LEVEL_PATH = "C:/Program Files/Git/Game/ArenaTools/Maps/Lvl_ArenaGen_Seed8"


def add_from_asset(asset_path, name, xform):
    return execute_tool(
        "editor_toolset.toolsets.scene.SceneTools.add_to_scene_from_asset",
        json.dumps({"asset_path": asset_path, "name": name, "xform": xform}))["returnValue"]


def add_from_class(class_path, name, xform):
    return execute_tool(
        "editor_toolset.toolsets.scene.SceneTools.add_to_scene_from_class",
        json.dumps({"actor_type": {"refPath": class_path}, "name": name,
                    "xform": xform}))["returnValue"]


def set_folder(actor, folder_path):
    execute_tool(
        "editor_toolset.toolsets.scene.SceneTools.set_actor_folder",
        json.dumps({"actor": actor, "folder_path": folder_path}))


def run():
    created = []
    failed = []
    for entry in PLACEMENTS:
        xform = {"location": entry["location"], "rotation": entry["rotation"]}
        if "scale" in entry:
            xform["scale"] = entry["scale"]
        try:
            if "asset_path" in entry:
                actor = add_from_asset(entry["asset_path"], entry["name"], xform)
            else:
                actor = add_from_class(entry["class_path"], entry["name"], xform)
            if entry.get("folder"):
                set_folder(actor, entry["folder"])
            created.append(entry["name"])
        except RuntimeError as exc:
            failed.append({"name": entry["name"], "error": str(exc)})
    execute_tool("editor_toolset.toolsets.asset.AssetTools.save_assets",
                 json.dumps({"asset_paths": []}))
    return {"level": LEVEL_PATH, "created": created, "failed": failed,
            "count": len(created)}
