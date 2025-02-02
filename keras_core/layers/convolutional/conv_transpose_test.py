import numpy as np
import pytest
from absl.testing import parameterized

from keras_core import backend
from keras_core import layers
from keras_core import testing
from keras_core.backend.common.backend_utils import (
    compute_conv_transpose_output_shape,
)
from keras_core.backend.common.backend_utils import (
    compute_conv_transpose_padding,
)


class ConvTransposeBasicTest(testing.TestCase, parameterized.TestCase):
    @parameterized.parameters(
        {
            "filters": 5,
            "kernel_size": 2,
            "strides": 2,
            "padding": "valid",
            "output_padding": None,
            "data_format": "channels_last",
            "dilation_rate": 1,
            "input_shape": (2, 8, 4),
            "output_shape": (2, 16, 5),
        },
        {
            "filters": 6,
            "kernel_size": 2,
            "strides": 3,
            "padding": "same",
            "output_padding": 2,
            "data_format": "channels_last",
            "dilation_rate": (1,),
            "input_shape": (2, 8, 4),
            "output_shape": (2, 23, 6),
        },
        {
            "filters": 6,
            "kernel_size": (2,),
            "strides": (2,),
            "padding": "valid",
            "output_padding": None,
            "data_format": "channels_last",
            "dilation_rate": 1,
            "input_shape": (2, 8, 4),
            "output_shape": (2, 16, 6),
        },
    )
    @pytest.mark.requires_trainable_backend
    def test_conv1d_transpose_basic(
        self,
        filters,
        kernel_size,
        strides,
        padding,
        output_padding,
        data_format,
        dilation_rate,
        input_shape,
        output_shape,
    ):
        self.run_layer_test(
            layers.Conv1DTranspose,
            init_kwargs={
                "filters": filters,
                "kernel_size": kernel_size,
                "strides": strides,
                "padding": padding,
                "output_padding": output_padding,
                "data_format": data_format,
                "dilation_rate": dilation_rate,
            },
            input_shape=input_shape,
            expected_output_shape=output_shape,
            expected_num_trainable_weights=2,
            expected_num_non_trainable_weights=0,
            expected_num_losses=0,
            supports_masking=False,
        )

    @parameterized.parameters(
        {
            "filters": 5,
            "kernel_size": 2,
            "strides": 2,
            "padding": "valid",
            "output_padding": None,
            "data_format": "channels_last",
            "dilation_rate": 1,
            "input_shape": (2, 8, 8, 4),
            "output_shape": (2, 16, 16, 5),
        },
        {
            "filters": 6,
            "kernel_size": 2,
            "strides": 3,
            "padding": "same",
            "output_padding": 2,
            "data_format": "channels_last",
            "dilation_rate": (1, 1),
            "input_shape": (2, 8, 8, 4),
            "output_shape": (2, 23, 23, 6),
        },
        {
            "filters": 6,
            "kernel_size": (2, 3),
            "strides": (2, 1),
            "padding": "valid",
            "output_padding": None,
            "data_format": "channels_first",
            "dilation_rate": (1, 1),
            "input_shape": (2, 4, 8, 8),
            "output_shape": (2, 6, 16, 10),
        },
        {
            "filters": 2,
            "kernel_size": (7, 7),
            "strides": (16, 16),
            "padding": "valid",
            "output_padding": None,
            "data_format": "channels_last",
            "dilation_rate": (1, 1),
            "input_shape": (1, 14, 14, 2),
            "output_shape": (1, 224, 224, 2),
        },
    )
    @pytest.mark.requires_trainable_backend
    def test_conv2d_transpose_basic(
        self,
        filters,
        kernel_size,
        strides,
        padding,
        output_padding,
        data_format,
        dilation_rate,
        input_shape,
        output_shape,
    ):
        if (
            data_format == "channels_first"
            and backend.backend() == "tensorflow"
        ):
            pytest.skip("channels_first unsupported on CPU with TF")

        self.run_layer_test(
            layers.Conv2DTranspose,
            init_kwargs={
                "filters": filters,
                "kernel_size": kernel_size,
                "strides": strides,
                "padding": padding,
                "output_padding": output_padding,
                "data_format": data_format,
                "dilation_rate": dilation_rate,
            },
            input_shape=input_shape,
            expected_output_shape=output_shape,
            expected_num_trainable_weights=2,
            expected_num_non_trainable_weights=0,
            expected_num_losses=0,
            supports_masking=False,
        )

    @parameterized.parameters(
        {
            "filters": 5,
            "kernel_size": 2,
            "strides": 2,
            "padding": "valid",
            "output_padding": None,
            "data_format": "channels_last",
            "dilation_rate": 1,
            "input_shape": (2, 8, 8, 8, 4),
            "output_shape": (2, 16, 16, 16, 5),
        },
        {
            "filters": 6,
            "kernel_size": 2,
            "strides": 3,
            "padding": "same",
            "output_padding": 2,
            "data_format": "channels_last",
            "dilation_rate": (1, 1, 1),
            "input_shape": (2, 8, 8, 8, 4),
            "output_shape": (2, 23, 23, 23, 6),
        },
        {
            "filters": 6,
            "kernel_size": (2, 2, 3),
            "strides": (2, 1, 2),
            "padding": "valid",
            "output_padding": None,
            "data_format": "channels_last",
            "dilation_rate": (1, 1, 1),
            "input_shape": (2, 8, 8, 8, 4),
            "output_shape": (2, 16, 9, 17, 6),
        },
    )
    @pytest.mark.requires_trainable_backend
    def test_conv3d_transpose_basic(
        self,
        filters,
        kernel_size,
        strides,
        padding,
        output_padding,
        data_format,
        dilation_rate,
        input_shape,
        output_shape,
    ):
        self.run_layer_test(
            layers.Conv3DTranspose,
            init_kwargs={
                "filters": filters,
                "kernel_size": kernel_size,
                "strides": strides,
                "padding": padding,
                "output_padding": output_padding,
                "data_format": data_format,
                "dilation_rate": dilation_rate,
            },
            input_shape=input_shape,
            expected_output_shape=output_shape,
            expected_num_trainable_weights=2,
            expected_num_non_trainable_weights=0,
            expected_num_losses=0,
            supports_masking=False,
        )

    def test_bad_init_args(self):
        # `filters` is not positive.
        with self.assertRaises(ValueError):
            layers.Conv1DTranspose(filters=0, kernel_size=1)

        # `kernel_size` has 0.
        with self.assertRaises(ValueError):
            layers.Conv2DTranspose(filters=2, kernel_size=(1, 0))

        # `strides` has 0.
        with self.assertRaises(ValueError):
            layers.Conv2DTranspose(
                filters=2, kernel_size=(2, 2), strides=(1, 0)
            )

        # `dilation_rate > 1` while `strides > 1`.
        with self.assertRaises(ValueError):
            layers.Conv2DTranspose(
                filters=2, kernel_size=(2, 2), strides=2, dilation_rate=(2, 1)
            )


class ConvTransposeCorrectnessTest(testing.TestCase, parameterized.TestCase):
    def np_conv1d_transpose(
        self,
        x,
        kernel_weights,
        bias_weights,
        strides,
        padding,
        output_padding,
        data_format,
        dilation_rate,
    ):
        if data_format == "channels_first":
            x = x.transpose((0, 2, 1))
        if isinstance(strides, (tuple, list)):
            h_stride = strides[0]
        else:
            h_stride = strides
        if isinstance(dilation_rate, (tuple, list)):
            h_dilation = dilation_rate[0]
        else:
            h_dilation = dilation_rate

        h_kernel, ch_out, ch_in = kernel_weights.shape
        n_batch, h_x, _ = x.shape
        # Get output shape and padding
        _, h_out, _ = compute_conv_transpose_output_shape(
            x.shape,
            kernel_weights.shape,
            ch_out,
            strides,
            padding,
            output_padding,
            data_format,
            dilation_rate,
        )
        (h_pad,) = compute_conv_transpose_padding(
            x.shape,
            kernel_weights.shape,
            strides,
            padding,
            output_padding,
            data_format,
            dilation_rate,
        )
        h_pad_side1 = h_kernel - 1 - h_pad[0]

        if h_dilation > 1:
            # Increase kernel size
            new_h_kernel = h_kernel + (h_dilation - 1) * (h_kernel - 1)
            new_kenel_size_tuple = (new_h_kernel,)
            new_kernel_weights = np.zeros(
                (*new_kenel_size_tuple, ch_out, ch_in),
                dtype=kernel_weights.dtype,
            )
            new_kernel_weights[::h_dilation] = kernel_weights
            kernel_weights = new_kernel_weights
            h_kernel = kernel_weights.shape[0]

        # Compute output
        output = np.zeros([n_batch, h_out + h_kernel, ch_out])
        for nb in range(n_batch):
            for h_x_idx in range(h_x):
                h_out_idx = h_x_idx * h_stride  # Index in output
                output[nb, h_out_idx : h_out_idx + h_kernel, :] += np.sum(
                    kernel_weights[:, :, :] * x[nb, h_x_idx, :], axis=-1
                )
        output = output + bias_weights

        # Cut padding results from output
        output = output[:, h_pad_side1 : h_out + h_pad_side1]
        if data_format == "channels_first":
            output = output.transpose((0, 2, 1))
        return output

    def np_conv2d_transpose(
        self,
        x,
        kernel_weights,
        bias_weights,
        strides,
        padding,
        output_padding,
        data_format,
        dilation_rate,
    ):
        if data_format == "channels_first":
            x = x.transpose((0, 2, 3, 1))
        if isinstance(strides, (tuple, list)):
            h_stride, w_stride = strides
        else:
            h_stride = strides
            w_stride = strides
        if isinstance(dilation_rate, (tuple, list)):
            h_dilation, w_dilation = dilation_rate
        else:
            h_dilation = dilation_rate
            w_dilation = dilation_rate

        h_kernel, w_kernel, ch_out, ch_in = kernel_weights.shape
        n_batch, h_x, w_x, _ = x.shape
        # Get output shape and padding
        _, h_out, w_out, _ = compute_conv_transpose_output_shape(
            x.shape,
            kernel_weights.shape,
            ch_out,
            strides,
            padding,
            output_padding,
            data_format,
            dilation_rate,
        )
        h_pad, w_pad = compute_conv_transpose_padding(
            x.shape,
            kernel_weights.shape,
            strides,
            padding,
            output_padding,
            data_format,
            dilation_rate,
        )
        h_pad_side1 = h_kernel - 1 - h_pad[0]
        w_pad_side1 = w_kernel - 1 - w_pad[0]

        if h_dilation > 1 or w_dilation > 1:
            # Increase kernel size
            new_h_kernel = h_kernel + (h_dilation - 1) * (h_kernel - 1)
            new_w_kernel = w_kernel + (w_dilation - 1) * (w_kernel - 1)
            new_kenel_size_tuple = (new_h_kernel, new_w_kernel)
            new_kernel_weights = np.zeros(
                (*new_kenel_size_tuple, ch_out, ch_in),
                dtype=kernel_weights.dtype,
            )
            new_kernel_weights[::h_dilation, ::w_dilation] = kernel_weights
            kernel_weights = new_kernel_weights
            h_kernel, w_kernel = kernel_weights.shape[:2]

        # Compute output
        output = np.zeros([n_batch, h_out + h_kernel, w_out + w_kernel, ch_out])
        for nb in range(n_batch):
            for h_x_idx in range(h_x):
                h_out_idx = h_x_idx * h_stride  # Index in output
                for w_x_idx in range(w_x):
                    w_out_idx = w_x_idx * w_stride
                    output[
                        nb,
                        h_out_idx : h_out_idx + h_kernel,
                        w_out_idx : w_out_idx + w_kernel,
                        :,
                    ] += np.sum(
                        kernel_weights[:, :, :, :] * x[nb, h_x_idx, w_x_idx, :],
                        axis=-1,
                    )
        output = output + bias_weights

        # Cut padding results from output
        output = output[
            :,
            h_pad_side1 : h_out + h_pad_side1,
            w_pad_side1 : w_out + w_pad_side1,
        ]
        if data_format == "channels_first":
            output = output.transpose((0, 3, 1, 2))
        return output

    def np_conv3d_transpose(
        self,
        x,
        kernel_weights,
        bias_weights,
        strides,
        padding,
        output_padding,
        data_format,
        dilation_rate,
    ):
        if data_format == "channels_first":
            x = x.transpose((0, 2, 3, 4, 1))
        if isinstance(strides, (tuple, list)):
            h_stride, w_stride, d_stride = strides
        else:
            h_stride = strides
            w_stride = strides
            d_stride = strides
        if isinstance(dilation_rate, (tuple, list)):
            h_dilation, w_dilation, d_dilation = dilation_rate
        else:
            h_dilation = dilation_rate
            w_dilation = dilation_rate
            d_dilation = dilation_rate

        h_kernel, w_kernel, d_kernel, ch_out, ch_in = kernel_weights.shape
        n_batch, h_x, w_x, d_x, _ = x.shape
        # Get output shape and padding
        _, h_out, w_out, d_out, _ = compute_conv_transpose_output_shape(
            x.shape,
            kernel_weights.shape,
            ch_out,
            strides,
            padding,
            output_padding,
            data_format,
            dilation_rate,
        )
        h_pad, w_pad, d_pad = compute_conv_transpose_padding(
            x.shape,
            kernel_weights.shape,
            strides,
            padding,
            output_padding,
            data_format,
            dilation_rate,
        )
        h_pad_side1 = h_kernel - 1 - h_pad[0]
        w_pad_side1 = w_kernel - 1 - w_pad[0]
        d_pad_side1 = d_kernel - 1 - d_pad[0]

        if h_dilation > 1 or w_dilation > 1 or d_dilation > 1:
            # Increase kernel size
            new_h_kernel = h_kernel + (h_dilation - 1) * (h_kernel - 1)
            new_w_kernel = w_kernel + (w_dilation - 1) * (w_kernel - 1)
            new_d_kernel = d_kernel + (d_dilation - 1) * (d_kernel - 1)
            new_kenel_size_tuple = (new_h_kernel, new_w_kernel, new_d_kernel)
            new_kernel_weights = np.zeros(
                (*new_kenel_size_tuple, ch_out, ch_in),
                dtype=kernel_weights.dtype,
            )
            new_kernel_weights[
                ::h_dilation, ::w_dilation, ::d_dilation
            ] = kernel_weights
            kernel_weights = new_kernel_weights
            h_kernel, w_kernel, d_kernel = kernel_weights.shape[:3]

        # Compute output
        output = np.zeros(
            [
                n_batch,
                h_out + h_kernel,
                w_out + w_kernel,
                d_out + d_kernel,
                ch_out,
            ]
        )
        for nb in range(n_batch):
            for h_x_idx in range(h_x):
                h_out_idx = h_x_idx * h_stride  # Index in output
                for w_x_idx in range(w_x):
                    w_out_idx = w_x_idx * w_stride
                    for d_x_idx in range(d_x):
                        d_out_idx = d_x_idx * d_stride
                        output[
                            nb,
                            h_out_idx : h_out_idx + h_kernel,
                            w_out_idx : w_out_idx + w_kernel,
                            d_out_idx : d_out_idx + d_kernel,
                            :,
                        ] += np.sum(
                            kernel_weights[:, :, :, :, :]
                            * x[nb, h_x_idx, w_x_idx, d_x_idx, :],
                            axis=-1,
                        )
        output = output + bias_weights

        # Cut padding results from output
        output = output[
            :,
            h_pad_side1 : h_out + h_pad_side1,
            w_pad_side1 : w_out + w_pad_side1,
            d_pad_side1 : d_out + d_pad_side1,
        ]
        if data_format == "channels_first":
            output = output.transpose((0, 4, 1, 2, 3))
        return output

    @parameterized.parameters(
        {
            "filters": 5,
            "kernel_size": 2,
            "strides": 2,
            "padding": "valid",
            "output_padding": None,
            "data_format": "channels_last",
            "dilation_rate": 1,
        },
        {
            "filters": 6,
            "kernel_size": 2,
            "strides": 3,
            "padding": "same",
            "output_padding": 2,
            "data_format": "channels_last",
            "dilation_rate": (1,),
        },
        {
            "filters": 6,
            "kernel_size": (2,),
            "strides": (2,),
            "padding": "valid",
            "output_padding": None,
            "data_format": "channels_last",
            "dilation_rate": 1,
        },
    )
    def test_conv1d_transpose(
        self,
        filters,
        kernel_size,
        strides,
        padding,
        output_padding,
        data_format,
        dilation_rate,
    ):
        layer = layers.Conv1DTranspose(
            filters=filters,
            kernel_size=kernel_size,
            strides=strides,
            padding=padding,
            output_padding=output_padding,
            data_format=data_format,
            dilation_rate=dilation_rate,
        )

        inputs = np.random.normal(size=[2, 8, 4])
        layer.build(input_shape=inputs.shape)

        kernel_shape = layer.kernel.shape
        kernel_weights = np.random.normal(size=kernel_shape)
        bias_weights = np.random.normal(size=(filters,))
        layer.kernel.assign(kernel_weights)
        layer.bias.assign(bias_weights)

        outputs = layer(inputs)
        expected = self.np_conv1d_transpose(
            inputs,
            kernel_weights,
            bias_weights,
            strides,
            padding,
            output_padding,
            data_format,
            dilation_rate,
        )
        self.assertAllClose(outputs, expected, atol=1e-5)

    @parameterized.parameters(
        {
            "filters": 5,
            "kernel_size": 2,
            "strides": 2,
            "padding": "valid",
            "output_padding": None,
            "data_format": "channels_last",
            "dilation_rate": 1,
        },
        {
            "filters": 6,
            "kernel_size": 7,
            "strides": 16,
            "padding": "same",
            "output_padding": 2,
            "data_format": "channels_last",
            "dilation_rate": (1, 1),
        },
        {
            "filters": 6,
            "kernel_size": (2, 3),
            "strides": (2, 1),
            "padding": "valid",
            "output_padding": None,
            "data_format": "channels_last",
            "dilation_rate": (1, 1),
        },
        {
            "filters": 2,
            "kernel_size": (7, 7),
            "strides": (16, 16),
            "padding": "valid",
            "output_padding": None,
            "data_format": "channels_last",
            "dilation_rate": (1, 1),
        },
    )
    def test_conv2d_transpose(
        self,
        filters,
        kernel_size,
        strides,
        padding,
        output_padding,
        data_format,
        dilation_rate,
    ):
        layer = layers.Conv2DTranspose(
            filters=filters,
            kernel_size=kernel_size,
            strides=strides,
            padding=padding,
            output_padding=output_padding,
            data_format=data_format,
            dilation_rate=dilation_rate,
        )

        inputs = np.random.normal(size=[2, 14, 14, 4])
        layer.build(input_shape=inputs.shape)

        kernel_shape = layer.kernel.shape
        kernel_weights = np.random.normal(size=kernel_shape)
        bias_weights = np.random.normal(size=(filters,))
        layer.kernel.assign(kernel_weights)
        layer.bias.assign(bias_weights)

        outputs = layer(inputs)
        expected = self.np_conv2d_transpose(
            inputs,
            kernel_weights,
            bias_weights,
            strides,
            padding,
            output_padding,
            data_format,
            dilation_rate,
        )
        self.assertAllClose(outputs, expected, atol=1e-5)

    @parameterized.parameters(
        {
            "filters": 5,
            "kernel_size": 2,
            "strides": 2,
            "padding": "valid",
            "output_padding": None,
            "data_format": "channels_last",
            "dilation_rate": 1,
        },
        {
            "filters": 6,
            "kernel_size": 2,
            "strides": 3,
            "padding": "same",
            "output_padding": 2,
            "data_format": "channels_last",
            "dilation_rate": (1, 1, 1),
        },
        {
            "filters": 6,
            "kernel_size": (2, 2, 3),
            "strides": (2, 1, 2),
            "padding": "valid",
            "output_padding": None,
            "data_format": "channels_last",
            "dilation_rate": (1, 1, 1),
        },
    )
    def test_conv3d_transpose(
        self,
        filters,
        kernel_size,
        strides,
        padding,
        output_padding,
        data_format,
        dilation_rate,
    ):
        layer = layers.Conv3DTranspose(
            filters=filters,
            kernel_size=kernel_size,
            strides=strides,
            padding=padding,
            output_padding=output_padding,
            data_format=data_format,
            dilation_rate=dilation_rate,
        )

        inputs = np.random.normal(size=[2, 8, 8, 8, 4])
        layer.build(input_shape=inputs.shape)

        kernel_shape = layer.kernel.shape
        kernel_weights = np.random.normal(size=kernel_shape)
        bias_weights = np.random.normal(size=(filters,))
        layer.kernel.assign(kernel_weights)
        layer.bias.assign(bias_weights)

        outputs = layer(inputs)
        expected = self.np_conv3d_transpose(
            inputs,
            kernel_weights,
            bias_weights,
            strides,
            padding,
            output_padding,
            data_format,
            dilation_rate,
        )
        self.assertAllClose(outputs, expected, atol=1e-5)
