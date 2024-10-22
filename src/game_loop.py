from src.render_object import RenderObject


class GameLoop:
    
    def scene_graph(
            self, 
            scene_node: RenderObject,
            transformations: list
            ) -> None:
        
        """
        A method that traverses the scene graph and applies '
        transformations to the nodes.
        
        Parameters:
        ----------
        scene_node : RenderObject
            The root node of the scene graph.
        transformations : list
            A list of transformations to apply to the nodes.
        """
        for transformation in transformations:
            transformation.apply(scene_node)
            
        scene_node.render()
        
        for child in scene_node.children:
            self.scene_graph(child, transformations)
        
        