import numpy as np
import pyrealsense2 as rs
import cv2


resolution_width, resolution_height = (640, 480)
clip_distance_max = 3.500  ##remove from the depth image all values above a given value (meters).


class DepthCamera:
    def __init__(self, resolution_width, resolution_height):
        # Configure depth and color streams
        self.pipeline = rs.pipeline()
        config = rs.config()

        # Get device product line for setting a supporting resolution
        pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
        pipeline_profile = config.resolve(pipeline_wrapper)
        device = pipeline_profile.get_device()
        depth_sensor = device.first_depth_sensor()
        # Get depth scale of the device
        self.depth_scale = depth_sensor.get_depth_scale()
        # Create an align object
        align_to = rs.stream.color

        self.align = rs.align(align_to)
        device_product_line = str(device.get_info(rs.camera_info.product_line))
        print("device product line:", device_product_line)
        config.enable_stream(rs.stream.depth, resolution_width, resolution_height, rs.format.z16, 6)
        config.enable_stream(rs.stream.color, resolution_width, resolution_height, rs.format.bgr8, 30)

        # Start streaming
        self.pipeline.start(config)

    def get_raw_frame(self):
        frames = self.pipeline.wait_for_frames()
        aligned_frames = self.align.process(frames)
        depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()
        if not depth_frame or not color_frame:
            return False, None, None
        return True, depth_frame, color_frame

    def get_depth_scale(self):
        """
        "scaling factor" refers to the relation between depth map units and meters;
        it has nothing to do with the focal length of the camera.
        Depth maps are typically stored in 16-bit unsigned integers at millimeter scale, thus to obtain Z value in meters, the depth map pixels need to be divided by 1000.
        """
        return self.depth_scale

    def release(self):
        self.pipeline.stop()


def depth2PointCloud(depth, depth_scale):
    intrinsics = depth.profile.as_video_stream_profile().intrinsics
    depth = np.asanyarray(depth.get_data()) * depth_scale  # 1000 mm => 0.001 meters
    rows, cols = depth.shape

    c, r = np.meshgrid(np.arange(cols), np.arange(rows), sparse=True)
    r = r.astype(float)
    c = c.astype(float)

    z = depth
    x = z * (c - intrinsics.ppx) / intrinsics.fx
    y = z * (r - intrinsics.ppy) / intrinsics.fy

    pointsxyz = np.dstack((x, y, z))

    return pointsxyz


# def main1():
#     Realsensed415Cam = DepthCamera(resolution_width, resolution_height)
#
#     depth_scale = Realsensed415Cam.get_depth_scale()
#
#     while True:
#
#         ret, depth_raw_frame, color_raw_frame = Realsensed415Cam.get_raw_frame()
#         if not ret:
#             print("Unable to get a frame")
#
#         points_xyz = depth2PointCloud(depth_raw_frame, depth_scale)
#         dst = calc_dist(points_xyz)
#
#         color_frame = np.asanyarray(color_raw_frame.get_data())
#         depth_frame = np.asanyarray(depth_raw_frame.get_data())
#
#         show(color_frame, depth_frame, dst)


def main():
    Realsensed415Cam = DepthCamera(resolution_width, resolution_height)

    depth_scale = Realsensed415Cam.get_depth_scale()

    while True:

        ret, depth_raw_frame, color_raw_frame = Realsensed415Cam.get_raw_frame()
        if not ret:
            print("Unable to get a frame")

        points_xyz_rgb = depth2PointCloud(depth_raw_frame, color_raw_frame, depth_scale, clip_distance_max)

        color_frame = np.asanyarray(color_raw_frame.get_data())
        depth_frame = np.asanyarray(depth_raw_frame.get_data())

        cv2.imshow("Frame", color_frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            cv2.imwrite("frame_color.png", color_frame)
            break

    Realsensed415Cam.release()  # release rs pipeline


if __name__ == '__main__':
    main()
